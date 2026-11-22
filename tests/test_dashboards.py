import pytest

def test_seeker_dashboard(client, app):
    with app.app_context():
        client.get("/demo-login/seeker")
        res = client.get("/seeker/dashboard")
        assert res.status_code == 200
        assert b"Welcome" in res.data
        assert b"Total Earnings" in res.data
        assert b"Recommended Shifts" in res.data

def test_employer_dashboard(client, app):
    with app.app_context():
        client.get("/demo-login/employer")
        res = client.get("/employer/dashboard")
        assert res.status_code == 200
        assert b"Active Shifts" in res.data
        assert b"Pending Applicants" in res.data

def test_admin_dashboard(client, app):
    with app.app_context():
        client.get("/demo-login/admin")
        res = client.get("/admin/dashboard")
        assert res.status_code == 200
        assert b"Control Center" in res.data or b"ADMIN CONSOLE" in res.data
        assert b"Flagged Incidents" in res.data
        assert b"Pending Merchant KYC" in res.data
