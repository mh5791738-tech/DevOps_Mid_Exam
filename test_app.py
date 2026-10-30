
import pytest
from app import app, submissions


@pytest.fixture
def client():
    app.config["TESTING"] = True

    # Clear old submissions before each test
    submissions.clear()

    with app.test_client() as client:
        yield client

    submissions.clear()


def test_valid_submission(client):
    response = client.post("/", data={
        "name": "Hamza Irfan",
        "reg_no": "FA23-BAI-010",
        "title": "DevOps Assignment",
        "url": "https://github.com"
    })

    assert response.status_code == 200
    assert b"Assignment submitted successfully!" in response.data
    assert len(submissions) == 2
    assert submissions[0]["reg_no"] == "FA23-BAI-010"


def test_missing_registration_number(client):
    response = client.post("/", data={
        "name": "Hamza Irfan",
        "reg_no": "",
        "title": "DevOps Assignment",
        "url": "https://github.com"
    })

    assert response.status_code == 200
    assert b"All fields are required." in response.data
    assert len(submissions) == 0


def test_invalid_url(client):
    response = client.post("/", data={
        "name": "Hamza Irfan",
        "reg_no": "FA23-BAI-010",
        "title": "DevOps Assignment",
        "url": "invalid-url"
    })

    assert response.status_code == 200
    assert b"Invalid submission URL." in response.data
    assert len(submissions) == 0
