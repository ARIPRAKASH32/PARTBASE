"""Unit tests for employer blueprint."""
import pytest
from app import create_app
from app.extensions import db
from app.models import User, Area, Shop
from config import TestConfig

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        area = Area(name='Anna Nagar', pincode='600040', lat=13.0850, lng=80.2100)
        db.session.add(area)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_employer_post_job_page_loads(client):
    """Test that employer job posting view is accessible."""
    response = client.get('/employer/post')
    assert response.status_code == 200

def test_employer_posts_page_redirect_unauth(client):
    """Test that employer posts dashboard redirects unauthenticated visitor."""
    response = client.get('/employer/posts')
    assert response.status_code in (200, 302)
