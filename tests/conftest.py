import pytest
from app import create_app
from app.extensions import db
from app.models import Area, User, Shop, Job
from config import TestConfig

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        area = Area(name='OMR', pincode='600096', lat=12.9249, lng=80.2272)
        db.session.add(area)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
