from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_signup_prevents_duplicate_registration():
    activity_name = "Chess Club"
    email = "duplicate@example.edu"
    original_participants = activities[activity_name]["participants"][:]
    activities[activity_name]["participants"] = []

    try:
        first_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )
        second_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        assert first_response.status_code == 200
        assert second_response.status_code == 400
        assert "already registered" in second_response.json()["detail"].lower()
    finally:
        activities[activity_name]["participants"] = original_participants


def test_unregister_participant_from_activity():
    activity_name = "Chess Club"
    email = "remove@example.edu"
    original_participants = activities[activity_name]["participants"][:]
    activities[activity_name]["participants"] = [email]

    try:
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants
