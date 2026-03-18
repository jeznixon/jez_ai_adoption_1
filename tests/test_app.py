import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Reset the in-memory activities before each test
    for activity in activities.values():
        if "participants" in activity:
            # Reset to original participants (could be improved for more isolation)
            if activity["description"].startswith("Learn strategies"):
                activity["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
            elif activity["description"].startswith("Learn programming"):
                activity["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
            elif activity["description"].startswith("Physical education"):
                activity["participants"] = ["john@mergington.edu", "olivia@mergington.edu"]
            elif activity["description"].startswith("Join the school soccer team"):
                activity["participants"] = ["alex@mergington.edu", "lucas@mergington.edu"]
            elif activity["description"].startswith("Practice basketball skills"):
                activity["participants"] = ["mia@mergington.edu", "noah@mergington.edu"]
            elif activity["description"].startswith("Act, direct, and produce"):
                activity["participants"] = ["ava@mergington.edu", "liam@mergington.edu"]
            elif activity["description"].startswith("Explore painting"):
                activity["participants"] = ["isabella@mergington.edu", "ethan@mergington.edu"]
            elif activity["description"].startswith("Prepare for math competitions"):
                activity["participants"] = ["charlotte@mergington.edu", "benjamin@mergington.edu"]
            elif activity["description"].startswith("Conduct experiments"):
                activity["participants"] = ["amelia@mergington.edu", "jack@mergington.edu"]


def test_get_activities():
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)


def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]


def test_signup_duplicate():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_activity_not_found():
    # Act
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_success():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unregister_not_found():
    # Arrange
    email = "notfound@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_unregister_activity_not_found():
    # Act
    response = client.delete("/activities/Nonexistent/unregister?email=someone@mergington.edu")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
