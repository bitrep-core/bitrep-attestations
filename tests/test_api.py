# Integration tests for API endpoints

import pytest
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_root_endpoint():
    """Test that server is running."""
    response = client.get("/docs")
    assert response.status_code == 200

def test_create_identity():
    """Test identity creation endpoint."""
    response = client.post(
        "/identity/create",
        json={"username": "test_user_1"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "public_key" in data
    assert "private_key" in data
    assert data["username"] == "test_user_1"

def test_create_duplicate_identity():
    """Test that duplicate username is rejected."""
    client.post("/identity/create", json={"username": "test_user_2"})
    
    # Try to create again
    response = client.post(
        "/identity/create",
        json={"username": "test_user_2"}
    )
    assert response.status_code == 400

def test_get_identity():
    """Test getting identity information."""
    # Create identity first
    create_response = client.post(
        "/identity/create",
        json={"username": "test_user_3"}
    )
    
    # Get identity
    response = client.get("/identity/test_user_3")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test_user_3"
    assert "public_key" in data

def test_create_attestation():
    """Test creating an attestation."""
    response = client.post(
        "/attest",
        json={
            "from_user": "alice",
            "to_user": "bob",
            "value": 5,
            "context": "Test attestation"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["from_user"] == "alice"
    assert data["to_user"] == "bob"
    assert data["value"] == 5

def test_get_user_reputation():
    """Test getting user reputation."""
    # Create some attestations
    client.post(
        "/attest",
        json={
            "from_user": "alice",
            "to_user": "user_rep_test",
            "value": 5,
            "context": "Good work"
        }
    )
    
    client.post(
        "/attest",
        json={
            "from_user": "bob",
            "to_user": "user_rep_test",
            "value": 3,
            "context": "Nice job"
        }
    )
    
    # Get reputation
    response = client.get("/user/user_rep_test")
    assert response.status_code == 200
    data = response.json()
    assert data["user"] == "user_rep_test"
    assert data["reputation"] >= 0
    assert len(data["attestations"]) == 2

def test_create_governance_proposal():
    """Test creating a governance proposal."""
    # Create identity first
    client.post("/identity/create", json={"username": "proposer_1"})
    
    response = client.post(
        "/governance/proposal",
        json={
            "title": "Test Proposal",
            "description": "A test governance proposal",
            "proposer": "proposer_1",
            "days_until_expiry": 7
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Proposal"
    assert data["status"] == "active"

def test_list_governance_proposals():
    """Test listing governance proposals."""
    response = client.get("/governance/proposals")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_prove_reputation_threshold():
    """Test zero-knowledge proof of reputation threshold."""
    # Create identity
    client.post("/identity/create", json={"username": "zk_test_user"})
    
    response = client.post(
        "/privacy/prove-threshold",
        json={
            "username": "zk_test_user",
            "threshold": 10.0
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "proof" in data
    assert "threshold" in data
    assert "verified" in data

def test_list_supported_platforms():
    """Test listing supported third-party platforms."""
    response = client.get("/integration/platforms")
    assert response.status_code == 200
    data = response.json()
    assert "supported_platforms" in data
    assert "github" in data["supported_platforms"]
    assert "ebay" in data["supported_platforms"]

def test_import_third_party_attestation():
    """Test importing third-party attestation."""
    # Create identity first
    client.post("/identity/create", json={"username": "import_test_user"})
    
    response = client.post(
        "/integration/import",
        json={
            "username": "import_test_user",
            "platform": "github",
            "platform_username": "githubuser",
            "attestation_type": "commits",
            "value": 50.0,
            "metadata": {"repo_count": 10}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["platform"] == "github"
    assert data["verified"] == 0  # Pending verification
