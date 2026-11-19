import pytest
from datetime import datetime, timedelta, timezone
from app import create_app
from app.extensions import db
from app.models import OTPRequest, User
from app.services.otp_service import OTPService
from config import TestConfig

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_otp_send_and_verify(app):
    phone = "+919876543210"
    res = OTPService.send_otp(phone, provider_name="console")
    assert res["ok"] is True
    code = res["debug_code"]
    assert len(code) == 6

    # Verify correct code
    verify_res = OTPService.verify_otp(phone, code)
    assert verify_res["ok"] is True
    assert verify_res["user_id"] is not None

def test_otp_resend_cooldown(app):
    phone = "+919876543211"
    res1 = OTPService.send_otp(phone)
    assert res1["ok"] is True

    # Immediate resend should be blocked by 30s cooldown
    res2 = OTPService.send_otp(phone)
    assert res2["ok"] is False
    assert res2["error"] == "COOLDOWN"

def test_otp_expiry(app):
    phone = "+919876543212"
    res = OTPService.send_otp(phone)
    code = res["debug_code"]

    # Artificially expire the OTP
    req = OTPRequest.query.filter_by(phone=phone).first()
    req.expires_at = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(minutes=1)
    db.session.commit()

    verify_res = OTPService.verify_otp(phone, code)
    assert verify_res["ok"] is False
    assert verify_res["error"] == "EXPIRED"

def test_otp_three_wrong_attempts_lockout(app):
    phone = "+919876543213"
    OTPService.send_otp(phone)

    # 3 wrong attempts
    OTPService.verify_otp(phone, "000000")
    OTPService.verify_otp(phone, "000000")
    res3 = OTPService.verify_otp(phone, "000000")
    assert res3["ok"] is False
    assert res3["error"] == "LOCKED"

    # Subsequent send or verify should also be locked
    send_res = OTPService.send_otp(phone)
    assert send_res["ok"] is False
    assert send_res["error"] == "LOCKED"
