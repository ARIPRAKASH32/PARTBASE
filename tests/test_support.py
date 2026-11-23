import pytest
from app.models import User, Ticket, Area
from app.extensions import db

def test_support_page_anonymous(client):
    res = client.get("/support")
    assert res.status_code == 200
    assert b"Support" in res.data or b"Trust" in res.data

def test_support_ticket_creation(client, app):
    with app.app_context():
        # Login demo seeker
        client.get("/demo-login/seeker")
        res = client.post("/support", data={
            "issue_type": "scam_fee_request",
            "description": "Store owner asked for registration fees upfront."
        }, follow_redirects=True)
        assert res.status_code == 200
        ticket = Ticket.query.filter_by(issue_type="scam_fee_request").first()
        assert ticket is not None
        assert "registration fees" in ticket.description
        assert ticket.status == "open"
