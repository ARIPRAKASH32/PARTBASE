import pytest
from app.models import SeekerProfile, User

def test_seeker_experience_page_get(client, app):
    with app.app_context():
        client.get("/demo-login/seeker")
        res = client.get("/seeker/experience")
        assert res.status_code == 200
        assert b"Work Experience &amp; Skills" in res.data
        assert b"Preferred Daily Working Hours" in res.data

def test_seeker_experience_post_update(client, app):
    with app.app_context():
        client.get("/demo-login/seeker")
        res = client.post("/seeker/experience", data={
            "experience_years": "2.5",
            "education_level": "College Student",
            "skills": "Fast Billing, Tally, Customer Care",
            "experience_summary": "2.5 years at Nilgiris supermarket managing billing counter.",
            "hours_per_day": "6",
            "interests": ["shop_helper", "packing"]
        }, follow_redirects=True)
        assert res.status_code == 200
        assert b"Work experience and hourly preferences updated successfully!" in res.data

        # Verify DB
        u = User.query.filter_by(phone="+919876511111").first()
        profile = u.seeker_profile
        assert profile.experience_years == 2.5
        assert profile.education_level == "College Student"
        assert profile.hours_per_day == 6
        assert "Tally" in profile.skills
