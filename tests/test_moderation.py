import pytest
from app import create_app
from app.extensions import db
from app.models import User, Area, Shop, Job, Report, Ticket, Rating
from app.utils.helpers import check_and_auto_hide_job, reveal_ratings_if_both_rated
from config import TestConfig

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_three_reports_auto_hides_job(app):
    area = Area(name="OMR", pincode="600096", lat=12.9352, lng=80.2290)
    db.session.add(area)
    db.session.commit()

    shop_owner = User(phone="+919876543210")
    db.session.add(shop_owner)
    db.session.commit()

    shop = Shop(owner_user_id=shop_owner.id, shop_name="Scam Shop", owner_name="Bad Actor", address="OMR", area_id=area.id)
    db.session.add(shop)
    db.session.commit()

    job = Job(shop_id=shop.id, category="data_entry", title="Typing job", pay_amount=200, status="open")
    db.session.add(job)
    db.session.commit()

    # Add 3 reports
    for i in range(3):
        u = User(phone=f"+91987650000{i}")
        db.session.add(u)
        db.session.commit()
        r = Report(job_id=job.id, reporter_id=u.id, reason="asked_money")
        db.session.add(r)
        db.session.commit()

    is_hidden = check_and_auto_hide_job(job.id)
    assert is_hidden is True
    assert job.status == "hidden"
    assert job.report_count == 3

def test_double_blind_rating_reveal(app):
    area = Area(name="OMR", pincode="600096", lat=12.9352, lng=80.2290)
    db.session.add(area)
    db.session.commit()

    employer = User(phone="+919876543210")
    seeker = User(phone="+919876511111")
    db.session.add_all([employer, seeker])
    db.session.commit()

    shop = Shop(owner_user_id=employer.id, shop_name="Tailor", owner_name="Owner", address="OMR", area_id=area.id)
    db.session.add(shop)
    db.session.commit()

    job = Job(shop_id=shop.id, category="shop_helper", title="Helper", pay_amount=100, status="completed")
    db.session.add(job)
    db.session.commit()

    # Step 1: Seeker rates shop
    r1 = Rating(
        job_id=job.id,
        rater_id=seeker.id,
        ratee_id=employer.id,
        direction="seeker_to_shop",
        stars=5,
        revealed=False
    )
    db.session.add(r1)
    db.session.commit()

    # Before employer rates, should remain unrevealed
    reveal_ratings_if_both_rated(job.id)
    assert r1.revealed is False

    # Step 2: Employer rates seeker
    r2 = Rating(
        job_id=job.id,
        rater_id=employer.id,
        ratee_id=seeker.id,
        direction="shop_to_seeker",
        stars=5,
        revealed=False
    )
    db.session.add(r2)
    db.session.commit()

    # Both have rated -> should reveal
    revealed = reveal_ratings_if_both_rated(job.id)
    assert revealed is True
    assert r1.revealed is True
    assert r2.revealed is True
