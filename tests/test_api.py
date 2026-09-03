from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities_returns_activity_data():
    response = client.get("/activities")

    assert response.status_code == 200
    assert "Chess Club" in response.json()
    assert response.json()["Chess Club"]["participants"]


def test_signup_adds_participant():
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 200
    assert email in client.get("/activities").json()["Chess Club"]["participants"]
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}


def test_signup_rejects_duplicate_participant():
    email = "michael@mergington.edu"

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_rejects_unknown_activity():
    response = client.post(
        "/activities/Unknown Club/signup?email=newstudent@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_participant():
    email = "newstudent@mergington.edu"
    client.post(f"/activities/Chess Club/signup?email={email}")

    response = client.delete(f"/activities/Chess Club/participants?email={email}")

    assert response.status_code == 200
    assert email not in client.get("/activities").json()["Chess Club"]["participants"]
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}


def test_unregister_rejects_unknown_participant():
    response = client.delete(
        "/activities/Chess Club/participants?email=unknown@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"
