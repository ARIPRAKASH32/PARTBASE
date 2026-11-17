import uuid
from datetime import datetime, timedelta
from app.extensions import db
from app.models import Payment, Job

class PaymentService:
    @staticmethod
    def boost_job(shop_id: int, job_id: int, method: str = "upi", provider_ref: str = None) -> dict:
        """
        Boosts a job for 24 hours with ₹49.
        Idempotent: If payment is already successful or job already boosted, prevents double charging.
        """
        job = Job.query.get(job_id)
        if not job:
            return {"ok": False, "error": "Job not found"}

        if job.shop_id != shop_id:
            return {"ok": False, "error": "Unauthorized: Not your shop job"}

        # Idempotency check: check if already boosted
        now = datetime.utcnow()
        if job.is_currently_boosted:
            return {
                "ok": True,
                "already_boosted": True,
                "message": "Job is already actively boosted for 24 hours.",
                "boost_expires_at": job.boost_expires_at.isoformat()
            }

        # Generate unique provider reference if not provided
        ref = provider_ref or f"UPI-MOCK-{uuid.uuid4().hex[:12].upper()}"

        # Prevent duplicate payment records
        existing_payment = Payment.query.filter_by(provider_ref=ref).first()
        if existing_payment:
            return {"ok": True, "message": "Payment already processed", "payment_id": existing_payment.id}

        payment = Payment(
            shop_id=shop_id,
            job_id=job.id,
            amount=49,
            method=method,
            status="success",
            provider_ref=ref
        )
        db.session.add(payment)

        # Apply boost to job
        job.is_boosted = True
        job.boost_expires_at = now + timedelta(hours=24)
        db.session.commit()

        return {
            "ok": True,
            "message": "Boost is live! Shop helper now shows first with an Urgent tag for 24 hours.",
            "payment_id": payment.id,
            "provider_ref": ref,
            "boost_expires_at": job.boost_expires_at.isoformat()
        }
