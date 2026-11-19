import pytest
from app.models import User, Area

def test_landing_page_loads(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"PARTBASE" in res.data
    assert b"Chennai" in res.data

def test_demo_login_seeker(client, app):
    with app.app_context():
        res = client.get("/demo-login/seeker", follow_redirects=True)
        assert res.status_code == 200
        assert b"Demo Seeker" in res.data or b"Priya" in res.data

def test_demo_login_employer(client, app):
    with app.app_context():
        res = client.get("/demo-login/employer", follow_redirects=True)
        assert res.status_code == 200
        assert b"Sri Murugan Tailors" in res.data or b"Employer" in res.data

def test_demo_login_admin(client, app):
    with app.app_context():
        res = client.get("/demo-login/admin", follow_redirects=True)
        assert res.status_code == 200
        assert b"Abuse Reports" in res.data or b"Admin" in res.data

def test_logout(client):
    client.get("/demo-login/seeker")
    res = client.get("/logout", follow_redirects=True)
    assert res.status_code == 200
    with client.session_transaction() as sess:
        assert "user_id" not in sess

def test_role_selection(client):
    res = client.get("/select-role/seeker", follow_redirects=True)
    assert res.status_code == 200
    with client.session_transaction() as sess:
        assert sess.get("role") == "seeker"
