import pytest
from app.models import User, Area, Shop, Job, Application, Rating
from app.extensions import db

def test_full_seeker_to_employer_hiring_lifecycle(client, app):
    with app.app_context():
        area = Area.query.first()

        # 1. Employer logs in and posts a shift
        client.get("/demo-login/employer")
        job = Job(
            shop_id=1,
            category="shop_helper",
            title="Evening Counter Assistant",
            day_option="today",
            pay_amount=150,
            pay_type="hour",
            people_needed=2,
            details="Assist customers at retail cash register.",
            status="open"
        )
        db.session.add(job)
        db.session.commit()
        job_id = job.id

        # 2. Seeker logs in and browses the job
        client.get("/demo-login/seeker")
        res = client.get(f"/seeker/jobs/{job_id}")
        assert res.status_code == 200
        assert b"Evening Counter Assistant" in res.data

        # 3. Seeker applies for the job
        res_apply = client.post(f"/seeker/jobs/{job_id}", data={
            "note": "I live 500m away in Thoraipakkam and can start at 5 PM."
        }, follow_redirects=True)
        assert res_apply.status_code == 200

        # Verify application created
        app_record = Application.query.filter_by(job_id=job_id).first()
        assert app_record is not None
        assert app_record.status == "applied"

        # 4. Employer views applicant list
        client.get("/demo-login/employer")
        res_employer = client.get(f"/employer/jobs/{job_id}")
        assert res_employer.status_code == 200
