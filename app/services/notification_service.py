import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class NotificationService:
    @staticmethod
    def notify_employer_new_application(job, application):
        logger.info(
            f"[Notification] Employer {job.shop.shop_name} ({job.shop.owner_name}): "
            f"New application received from {application.seeker.name or 'Seeker'} for '{job.title}'."
        )

    @staticmethod
    def notify_seeker_hired(job, seeker):
        logger.info(
            f"[Notification] Seeker {seeker.name} ({seeker.phone}): "
            f"You are HIRED for '{job.title}' at {job.shop.shop_name}! Address: {job.shop.address}."
        )

    @staticmethod
    def notify_reporters_job_removed(job_id, reason="Safety policy violation"):
        from app.models import Report, Ticket
        from app.extensions import db
        reports = Report.query.filter_by(job_id=job_id).all()
        for r in reports:
            logger.info(
                f"[Notification] User {r.reporter_id}: "
                f"The job you reported has been removed by our moderation team. Reason: {reason}."
            )
            if r.ticket_id:
                ticket = db.session.get(Ticket, r.ticket_id)
                if ticket:
                    ticket.status = "resolved"
                    ticket.admin_reply = f"Thank you for reporting. This job was investigated and removed: {reason}."
        db.session.commit()
