"""
Pytest configuration and shared fixtures for the test suite.
"""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities as original_activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def activities(monkeypatch):
    """
    Provide a fresh copy of activities for each test.
    
    This fixture uses monkeypatch to replace the module-level activities dict
    with a deep copy, ensuring test isolation and preventing cross-test pollution.
    """
    # Create a deep copy of the original activities
    activities_copy = deepcopy(original_activities)
    
    # Replace the module-level activities dict in src.app
    monkeypatch.setattr("src.app.activities", activities_copy)
    
    return activities_copy
