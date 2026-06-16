"""
Test suite for Mergington High School Activities API.

Tests use the AAA (Arrange-Act-Assert) pattern for clarity:
- Arrange: Set up test data and preconditions
- Act: Execute the API call or operation
- Assert: Verify the results match expectations
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client, activities):
        """
        Verify that GET /activities returns all available activities.
        
        AAA Pattern:
        - Arrange: Activities fixture provides initial data
        - Act: Call GET /activities endpoint
        - Assert: Response contains all activity names and correct structure
        """
        # Arrange
        expected_activities = list(activities.keys())
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert set(result.keys()) == set(expected_activities)
        assert len(result) > 0
        
        # Verify structure of each activity
        for activity_name, activity_data in result.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_valid_activity(self, client, activities):
        """
        Verify that a student can sign up for a valid activity.
        
        AAA Pattern:
        - Arrange: Identify a valid activity and new email
        - Act: POST signup request
        - Assert: Status is 200, participant is added, message is correct
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "alice@mergington.edu"
        initial_count = len(activities[activity_name]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["message"] == f"Signed up {new_email} for {activity_name}"
        assert new_email in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count + 1

    def test_signup_duplicate_email(self, client, activities):
        """
        Verify that signing up twice with the same email returns 400 error.
        
        AAA Pattern:
        - Arrange: Get an existing participant from an activity
        - Act: Try to sign up the same participant again
        - Assert: Status is 400, error detail mentions already signed up
        """
        # Arrange
        activity_name = "Chess Club"
        existing_email = activities[activity_name]["participants"][0]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        # Assert
        assert response.status_code == 400
        result = response.json()
        assert "already signed up" in result["detail"]

    def test_signup_invalid_activity(self, client, activities):
        """
        Verify that signing up for a nonexistent activity returns 404 error.
        
        AAA Pattern:
        - Arrange: Use a fake activity name
        - Act: POST signup for nonexistent activity
        - Assert: Status is 404, error detail mentions activity not found
        """
        # Arrange
        fake_activity = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{fake_activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "Activity not found" in result["detail"]


class TestUnregister:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_valid_participant(self, client, activities):
        """
        Verify that a participant can be unregistered from an activity.
        
        AAA Pattern:
        - Arrange: Get an existing participant and their activity
        - Act: DELETE unregister request
        - Assert: Status is 200, participant is removed, message is correct
        """
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = activities[activity_name]["participants"][0]
        initial_count = len(activities[activity_name]["participants"])
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email_to_remove}
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["message"] == f"Unregistered {email_to_remove} from {activity_name}"
        assert email_to_remove not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count - 1

    def test_unregister_invalid_participant(self, client, activities):
        """
        Verify that unregistering a nonexistent participant returns 404 error.
        
        AAA Pattern:
        - Arrange: Use an email not in any activity's participants
        - Act: DELETE unregister for nonexistent participant
        - Assert: Status is 404, error detail mentions participant not found
        """
        # Arrange
        activity_name = "Chess Club"
        fake_email = "nonexistent@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": fake_email}
        )
        
        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "Participant not found" in result["detail"]

    def test_unregister_invalid_activity(self, client, activities):
        """
        Verify that unregistering from a nonexistent activity returns 404 error.
        
        AAA Pattern:
        - Arrange: Use a fake activity name
        - Act: DELETE unregister from nonexistent activity
        - Assert: Status is 404, error detail mentions activity not found
        """
        # Arrange
        fake_activity = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{fake_activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "Activity not found" in result["detail"]


class TestRootRedirect:
    """Tests for GET / endpoint."""

    def test_root_redirect(self, client):
        """
        Verify that GET / redirects to /static/index.html.
        
        AAA Pattern:
        - Arrange: Prepare client with follow_redirects disabled
        - Act: GET / endpoint
        - Assert: Status is 307 (temporary redirect), location header points to /static/index.html
        """
        # Arrange
        # TestClient follows redirects by default, so we test the redirect response
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
