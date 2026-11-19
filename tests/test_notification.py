"""Unit tests for notification service."""
import pytest
from app import create_app
from app.extensions import db
from app.models import User, Ticket, Report
from app.services.notification_service import NotificationService
from config import TestConfig

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_notify_reporters_job_removed(app):
    """Test notifying reporters when flagged job is removed and resolving ticket."""
    user = User(phone="+919876500000", active_role="seeker", is_phone_verified=True)
    db.session.add(user)
    db.session.commit()

    ticket = Ticket(
        raised_by_id=user.id,
        role="seeker",
        issue_type="scam_fee_request",
        description="Asked deposit money",
        status="open"
    )
    db.session.add(ticket)
    db.session.commit()

    report = Report(reporter_id=user.id, job_id=99, reason="registration_fee", ticket_id=ticket.id)
    db.session.add(report)
    db.session.commit()

    NotificationService.notify_reporters_job_removed(job_id=99, reason="Violated zero-fee policy")

    updated_ticket = db.session.get(Ticket, ticket.id)
    assert updated_ticket.status == "resolved"
    assert "Violated zero-fee policy" in updated_ticket.admin_reply
