# Tests for cryptographic utilities

import pytest
from utils.crypto import (
    generate_keypair,
    sign_attestation,
    verify_signature,
    hash_private_key
)

def test_generate_keypair():
    """Test key pair generation."""
    public_key, private_key = generate_keypair()
    
    assert public_key is not None
    assert private_key is not None
    assert "BEGIN PUBLIC KEY" in public_key
    assert "BEGIN PRIVATE KEY" in private_key
    assert public_key != private_key

def test_sign_and_verify_attestation():
    """Test signing and verification of attestations."""
    # Generate key pair
    public_key, private_key = generate_keypair()
    
    # Sample attestation data
    attestation_data = {
        "from_user": "alice",
        "to_user": "bob",
        "value": 5,
        "context": "Test attestation"
    }
    
    # Sign attestation
    signature = sign_attestation(attestation_data, private_key)
    assert signature is not None
    assert len(signature) > 0
    
    # Verify signature
    is_valid = verify_signature(attestation_data, signature, public_key)
    assert is_valid is True

def test_verify_invalid_signature():
    """Test verification of invalid signature."""
    public_key, private_key = generate_keypair()
    
    attestation_data = {
        "from_user": "alice",
        "to_user": "bob",
        "value": 5,
        "context": "Test attestation"
    }
    
    # Sign attestation
    signature = sign_attestation(attestation_data, private_key)
    
    # Modify data
    modified_data = attestation_data.copy()
    modified_data["value"] = 10
    
    # Verification should fail
    is_valid = verify_signature(modified_data, signature, public_key)
    assert is_valid is False

def test_hash_private_key():
    """Test private key hashing."""
    _, private_key = generate_keypair()
    
    hash1 = hash_private_key(private_key)
    hash2 = hash_private_key(private_key)
    
    # Same key should produce same hash
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA256 hex digest is 64 characters
