import pytest
from app.models import User, Shop, Job, Report, AuditLog
from app.extensions import db

def test_admin_access_unauthorized(client):
    res = client.get("/admin/reports", follow_redirects=False)
    assert res.status_code == 302
    assert "/admin/login" in res.headers["Location"]

def test_admin_reports_authorized(client, app):
    with app.app_context():
        client.get("/demo-login/admin")
        res = client.get("/admin/reports")
        assert res.status_code == 200
        assert b"Job Abuse" in res.data or b"Flagged" in res.data

def test_admin_shops_page(client, app):
    with app.app_context():
        client.get("/demo-login/admin")
        res = client.get("/admin/employers")
        assert res.status_code == 200
        assert b"Shop" in res.data or b"Merchant" in res.data or b"Verifications" in res.data

def test_admin_support_inbox(client, app):
    with app.app_context():
        client.get("/demo-login/admin")
        res = client.get("/admin/support")
        assert res.status_code == 200
