from fastapi.testclient import TestClient
from urllib.parse import quote
from src.app import app

client = TestClient(app)


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_and_remove_participant():
    activity = "Chess Club"
    email = "pytest_user@example.com"

    # ensure not present
    r = client.get("/activities")
    assert email not in r.json()[activity]["participants"]

    # sign up
    r = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert r.status_code == 200
    assert "Signed up" in r.json().get("message", "")

    # should now be present
    r = client.get("/activities")
    assert email in r.json()[activity]["participants"]

    # remove
    r = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})
    assert r.status_code == 200
    assert "Removed" in r.json().get("message", "")

    # should be gone
    r = client.get("/activities")
    assert email not in r.json()[activity]["participants"]
