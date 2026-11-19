"""Unit tests for seeker blueprint."""
import pytest
from app import create_app
from app.extensions import db
from app.models import Area
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

def test_seeker_jobs_page_status(client):
    """Test that jobs listing page loads with HTTP 200."""
    response = client.get('/seeker/jobs')
    assert response.status_code == 200
    assert b"PARTBASE" in response.data

def test_seeker_jobs_filter_by_day(client):
    """Test filtering jobs by day option."""
    response = client.get('/seeker/jobs?day=today')
    assert response.status_code == 200

def test_seeker_jobs_filter_by_category(client):
    """Test filtering jobs by category."""
    response = client.get('/seeker/jobs?category=shop_helper')
    assert response.status_code == 200
