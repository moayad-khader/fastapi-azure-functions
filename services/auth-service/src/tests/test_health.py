"""Tests for health endpoints."""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.app import app

client = TestClient(app)


def test_health_check():
    """Test basic health check endpoint."""
    response = client.get("/health/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Service is healthy"
    assert "data" in data
    assert data["data"]["service"] == "auth-service"
    assert data["data"]["status"] == "healthy"


def test_readiness_check():
    """Test readiness check endpoint."""
    response = client.get("/health/ready")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert data["data"]["service"] == "auth-service"
    assert "checks" in data["data"]


def test_liveness_check():
    """Test liveness check endpoint."""
    response = client.get("/health/live")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Service is alive"
    assert data["data"]["service"] == "auth-service"
    assert data["data"]["status"] == "alive"
