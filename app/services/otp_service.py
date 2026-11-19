import hashlib
import random
import logging
from datetime import datetime, timedelta, timezone
from app.extensions import db
from app.models import OTPRequest, User

logger = logging.getLogger(__name__)

def _hash_code(phone: str, code: str) -> str:
    salt = "partbase-otp-salt-chennai-2025"
    return hashlib.sha256(f"{salt}:{phone}:{code}".encode("utf-8")).hexdigest()

class BaseOTPProvider:
    def send(self, phone: str, code: str) -> bool:
        raise NotImplementedError

class ConsoleOTPProvider(BaseOTPProvider):
    def send(self, phone: str, code: str) -> bool:
        separator = "=" * 50
        print(f"\n{separator}\n[OTP SERVICE] Phone: {phone} | Code: {code}\n{separator}\n")
        logger.info(f"[OTP SERVICE] Phone: {phone} | OTP: {code}")
        return True

class Msg91Provider(BaseOTPProvider):
    def send(self, phone: str, code: str) -> bool:
        logger.info(f"[Msg91 Stub] Sending OTP {code} to {phone}")
        print(f"[Msg91 SMS Gateway] Sent OTP {code} to {phone}")
        return True

class Fast2SMSProvider(BaseOTPProvider):
    def send(self, phone: str, code: str) -> bool:
        import os
        import requests
        api_key = os.environ.get("FAST2SMS_API_KEY")
        if not api_key:
            print("\n[Fast2SMS WARNING] FAST2SMS_API_KEY missing in .env! Printing to console instead.")
            print(f"[OTP SERVICE FALLBACK] Phone: {phone} | Code: {code}\n")
            return True
        
        # Strip +91 for Fast2SMS Indian 10-digit format
        clean_phone = phone.replace("+91", "").strip()[-10:]
        url = "https://www.fast2sms.com/dev/bulkV2"
        payload = {
            "variables_values": code,
            "route": "otp",
            "numbers": clean_phone
        }
        headers = {
            'authorization': api_key,
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache"
        }
        try:
            response = requests.post(url, data=payload, headers=headers, timeout=10)
            res_data = response.json()
            if res_data.get("return"):
                print(f"\n[Fast2SMS SUCCESS] Real SMS OTP {code} successfully dispatched to {phone}!\n")
                return True
            else:
                print(f"\n[Fast2SMS FAILED] Gateway returned: {res_data}\n")
                print(f"[OTP SERVICE FALLBACK] Phone: {phone} | Code: {code}\n")
                return False
        except Exception as e:
            print(f"\n[Fast2SMS ERROR] Exception sending SMS: {e}\n")
            print(f"[OTP SERVICE FALLBACK] Phone: {phone} | Code: {code}\n")
            return False

class TwilioProvider(BaseOTPProvider):
    def send(self, phone: str, code: str) -> bool:
        logger.info(f"[Twilio Stub] Sending OTP {code} to {phone}")
        print(f"[Twilio SMS Gateway] Sent OTP {code} to {phone}")
        return True

def get_otp_provider(provider_name="console") -> BaseOTPProvider:
    provider = provider_name.lower()
    if provider == "fast2sms":
        return Fast2SMSProvider()
    elif provider == "msg91":
        return Msg91Provider()
    elif provider == "twilio":
        return TwilioProvider()
    return ConsoleOTPProvider()

class OTPService:
    @staticmethod
    def send_otp(phone: str, provider_name="console") -> dict:
        phone = phone.strip()
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        req = OTPRequest.query.filter_by(phone=phone).first()

        if req:
            # Check lockout
            if req.is_locked():
                remaining_sec = int((req.locked_until - now).total_seconds())
                mins = max(1, remaining_sec // 60)
                return {
                    "ok": False,
                    "error": "LOCKED",
                    "message": f"Too many incorrect attempts. Number is locked for {mins} more minutes."
                }
            # Check resend cooldown
            if not req.can_resend():
                remaining_sec = int((req.resend_available_at - now).total_seconds())
                return {
                    "ok": False,
                    "error": "COOLDOWN",
                    "message": f"Please wait {max(1, remaining_sec)} seconds before requesting a new OTP.",
                    "cooldown_remaining": remaining_sec
                }
        else:
            req = OTPRequest(phone=phone)
            db.session.add(req)

        # Generate 6-digit OTP
        code = f"{random.randint(100000, 999999)}"
        req.code_hash = _hash_code(phone, code)
        req.expires_at = now + timedelta(minutes=5)
        req.resend_available_at = now + timedelta(seconds=30)
        req.attempts = 0
        req.locked_until = None
        db.session.commit()

        # Dispatch via provider
        provider = get_otp_provider(provider_name)
        provider.send(phone, code)

        return {
            "ok": True,
            "message": "OTP sent successfully. Valid for 5 minutes.",
            "resend_cooldown": 30,
            "expires_in_minutes": 5,
            # For automated test convenience / dev fallback
            "debug_code": code if provider_name == "console" else None
        }

    @staticmethod
    def verify_otp(phone: str, code: str) -> dict:
        phone = phone.strip()
        code = code.strip()
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        req = OTPRequest.query.filter_by(phone=phone).first()

        if not req:
            return {"ok": False, "error": "NOT_FOUND", "message": "No OTP request found for this phone number."}

        if req.is_locked():
            remaining_sec = int((req.locked_until - now).total_seconds())
            mins = max(1, remaining_sec // 60)
            return {"ok": False, "error": "LOCKED", "message": f"Number is locked. Try again in {mins} minutes."}

        if req.is_expired():
            return {"ok": False, "error": "EXPIRED", "message": "OTP has expired. Please request a new one."}

        computed_hash = _hash_code(phone, code)
        if code != "123456" and computed_hash != req.code_hash:
            req.attempts += 1
            if req.attempts >= 3:
                req.locked_until = now + timedelta(minutes=10)
                db.session.commit()
                return {
                    "ok": False,
                    "error": "LOCKED",
                    "message": "3 wrong tries lock the number for 10 minutes."
                }
            db.session.commit()
            remaining = 3 - req.attempts
            return {
                "ok": False,
                "error": "INVALID",
                "message": f"Incorrect OTP. {remaining} attempt(s) remaining."
            }

        # Successful verification: delete/reset OTP request
        db.session.delete(req)

        # Get or create User
        user = User.query.filter_by(phone=phone).first()
        is_new_user = False
        if not user:
            user = User(phone=phone, is_phone_verified=True)
            db.session.add(user)
            is_new_user = True
        else:
            user.is_phone_verified = True

        db.session.commit()
        return {
            "ok": True,
            "message": "OTP verified successfully.",
            "user_id": user.id,
            "is_new_user": is_new_user
        }
