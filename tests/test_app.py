# tests/test_app.py
import pytest
from app import create_app
from flask import url_for

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_page(client):
    """Test that the login page loads."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Login" in response.data

def test_valid_login(client):
    """Test logging in with default credentials from data.json."""
    response = client.post('/', data={
        'account_number': '1001',
        'password': '1234'
    }, follow_redirects=True)
    assert b"Welcome to the Dashboard" in response.data

def test_story_generation_no_auth(client):
    """Test that generating a story without login redirects to login."""
    response = client.post('/generate-story', data={
        'theme': 'Adventure in the forest',
        'word_count': '50'
    }, follow_redirects=True)
    assert b"Login" in response.data