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
        from app.models import Job, Application, User, Shop
        from app.extensions import db
        client.get("/demo-login/employer")
        
        # Add test applicant to verify applicant_profile url_for resolution
        shop = Shop.query.first()
        if shop:
            job = Job.query.filter_by(shop_id=shop.id).first()
            seeker = User.query.filter_by(phone="+919876511111").first()
            if job and seeker and not Application.query.filter_by(job_id=job.id, seeker_id=seeker.id).first():
                app_rec = Application(job_id=job.id, seeker_id=seeker.id, note="Ready to help")
                db.session.add(app_rec)
                db.session.commit()

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
