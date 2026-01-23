# Test configuration and fixtures

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.connection import Base
from main import app
import os

# Create test database
TEST_DATABASE_URL = "sqlite:///./test_bitrep.db"

@pytest.fixture(scope="module")
def test_db():
    """Create a test database."""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    # Clean up test database
    if os.path.exists("./test_bitrep.db"):
        os.remove("./test_bitrep.db")

@pytest.fixture(scope="module")
def client(test_db):
    """Create a test client."""
    return TestClient(app)

@pytest.fixture
def sample_identity():
    """Sample identity data for testing."""
    return {
        "username": "test_user",
        "public_key": "test_public_key",
        "verified": False,
        "reputation_score": 0.0
    }

@pytest.fixture
def sample_attestation():
    """Sample attestation data for testing."""
    return {
        "from_user": "alice",
        "to_user": "bob",
        "value": 5,
        "context": "Delivered product on time"
    }
