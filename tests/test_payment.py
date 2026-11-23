"""Unit tests for payment boost service."""
import pytest
from app import create_app
from app.extensions import db
from app.models import User, Area, Shop, Job, Payment
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

def test_boost_job_success(app):
    """Test successful job boost payment creation."""
    area = Area(name="Perungudi", pincode="600096", lat=12.9654, lng=80.2461)
    db.session.add(area)
    db.session.commit()

    user = User(phone="+919800000001", active_role="employer", is_phone_verified=True)
    db.session.add(user)
    db.session.commit()

    shop = Shop(owner_user_id=user.id, shop_name="Perungudi Supermarket", owner_name="Owner", area_id=area.id, address="OMR Rd")
    db.session.add(shop)
    db.session.commit()

    job = Job(
        shop_id=shop.id,
        title="Packing Staff",
        category="packing",
        day_option="today",
        pay_amount=150,
        pay_type="hour"
    )
    db.session.add(job)
    db.session.commit()

    res = PaymentService.boost_job(shop_id=shop.id, job_id=job.id)
    assert res["ok"] is True
    assert job.is_boosted is True
    assert job.is_currently_boosted is True
