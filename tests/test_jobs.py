import pytest
from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models import User, Area, Shop, Job, Application
from app.utils.geo import haversine_distance
from app.services.payment_service import PaymentService
from config import TestConfig

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_haversine_distance_calculation(app):
    # Thoraipakkam to Neelankarai distance (~2.2 km)
    dist = haversine_distance(12.9431, 80.2376, 12.9492, 80.2543)
    assert 1.5 <= dist <= 3.0

def test_boost_job_idempotency(app):
    area = Area(name="OMR", pincode="600096", lat=12.9352, lng=80.2290)
    db.session.add(area)
    db.session.commit()

    user = User(phone="+919876543210", active_role="employer", is_phone_verified=True)
    db.session.add(user)
    db.session.commit()

    shop = Shop(owner_user_id=user.id, shop_name="Test Shop", owner_name="Owner", address="OMR", area_id=area.id)
    db.session.add(shop)
    db.session.commit()

    job = Job(shop_id=shop.id, category="shop_helper", title="Counter help", pay_amount=100, status="open")
    db.session.add(job)
    db.session.commit()

    # First boost
    res1 = PaymentService.boost_job(shop_id=shop.id, job_id=job.id, method="upi")
    assert res1["ok"] is True
    assert job.is_boosted is True

    # Duplicate boost attempt within 24h should be idempotent
    res2 = PaymentService.boost_job(shop_id=shop.id, job_id=job.id, method="upi")
    assert res2["ok"] is True
    assert res2.get("already_boosted") is True

def test_hire_count_and_auto_close(app):
    area = Area(name="OMR", pincode="600096", lat=12.9352, lng=80.2290)
    db.session.add(area)
    db.session.commit()

    shop_owner = User(phone="+919876543210", active_role="employer")
    seeker1 = User(phone="+919876511111", active_role="seeker")
    db.session.add_all([shop_owner, seeker1])
    db.session.commit()

    shop = Shop(owner_user_id=shop_owner.id, shop_name="Tailor", owner_name="Murugan", address="OMR", area_id=area.id)
    db.session.add(shop)
    db.session.commit()

    job = Job(shop_id=shop.id, category="shop_helper", title="Helper", pay_amount=100, people_needed=1, hired_count=0, status="open")
    db.session.add(job)
    db.session.commit()

    app_entry = Application(job_id=job.id, seeker_id=seeker1.id, status="applied")
    db.session.add(app_entry)
    db.session.commit()

    # Hire seeker
    app_entry.status = "hired"
    job.hired_count += 1
    if job.hired_count >= job.people_needed:
        job.status = "closed"
    db.session.commit()

    assert job.hired_count == 1
    assert job.status == "closed"
