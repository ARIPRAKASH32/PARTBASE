import pytest
from app.models import User, Area, Shop, Job, Application, Rating, Payment
from app.extensions import db

def test_user_creation_and_repr(app):
    with app.app_context():
        u = User(phone="+919999988888", name="Kavitha M", is_phone_verified=True, active_role="seeker")
        db.session.add(u)
        db.session.commit()
        assert str(u) == f"<User {u.id}>"
        assert u.id is not None

def test_shop_relationship_with_user(app):
    with app.app_context():
        area = Area.query.first()
        u = User(phone="+919999977777", name="Gopal K", is_phone_verified=True, active_role="employer")
        db.session.add(u)
        db.session.commit()

        shop = Shop(owner_user_id=u.id, shop_name="Gopal Provisions", owner_name="Gopal", address="10 High Road", area_id=area.id)
        db.session.add(shop)
        db.session.commit()

        assert u.shop is not None
        assert u.shop.shop_name == "Gopal Provisions"
        assert u.shop.owner_user_id == u.id

def test_job_application_flow(app):
    with app.app_context():
        area = Area.query.first()
        owner = User(phone="+919999966666", name="Owner", is_phone_verified=True, active_role="employer")
        seeker = User(phone="+919999955555", name="Seeker", is_phone_verified=True, active_role="seeker")
        db.session.add_all([owner, seeker])
        db.session.commit()

        shop = Shop(owner_user_id=owner.id, shop_name="Test Store", owner_name="Owner", address="Test St", area_id=area.id)
        db.session.add(shop)
        db.session.commit()

        job = Job(shop_id=shop.id, category="shop_helper", title="Store Helper", day_option="today", pay_amount=500, pay_type="day", people_needed=1, status="open")
        db.session.add(job)
        db.session.commit()

        app_record = Application(job_id=job.id, seeker_id=seeker.id, note="Ready to work", status="applied")
        db.session.add(app_record)
        db.session.commit()

        assert len(job.applications) == 1
        assert job.applications[0].seeker_id == seeker.id
