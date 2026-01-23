# Tests for reputation calculation algorithms

import pytest
from utils.reputation import (
    calculate_weighted_reputation,
    calculate_attestation_weight,
    detect_isolated_clusters,
    apply_time_decay
)
import math

def test_calculate_weighted_reputation_simple():
    """Test basic weighted reputation calculation."""
    attestations = [
        ("alice", "bob", 5, 1.0),
        ("charlie", "bob", 3, 1.0),
    ]
    
    reputation = calculate_weighted_reputation(attestations)
    
    assert "bob" in reputation
    assert reputation["bob"] > 0
    assert "alice" in reputation
    assert "charlie" in reputation

def test_calculate_weighted_reputation_chain():
    """Test reputation propagation through attestation chain."""
    attestations = [
        ("alice", "bob", 5, 1.0),
        ("bob", "charlie", 3, 1.0),
    ]
    
    reputation = calculate_weighted_reputation(attestations)
    
    # Charlie's reputation should be influenced by Alice through Bob
    assert reputation["charlie"] > 0

def test_calculate_attestation_weight():
    """Test attestation weight calculation."""
    # Low reputation
    weight1 = calculate_attestation_weight(1.0)
    # High reputation
    weight2 = calculate_attestation_weight(100.0)
    
    # Higher reputation should produce higher weight
    assert weight2 > weight1
    assert weight1 > 0

def test_calculate_attestation_weight_with_discount():
    """Test attestation weight with cluster discount."""
    base_weight = calculate_attestation_weight(50.0, cluster_discount=1.0)
    discounted_weight = calculate_attestation_weight(50.0, cluster_discount=0.5)
    
    # Discounted weight should be lower
    assert discounted_weight < base_weight

def test_detect_isolated_clusters():
    """Test detection of isolated attestation clusters."""
    # Create a network with an isolated cluster
    attestations = [
        ("alice", "bob", 1, 1.0),
        ("bob", "alice", 1, 1.0),
        # Isolated cluster
        ("carol", "dave", 1, 1.0),
        ("dave", "carol", 1, 1.0),
    ]
    
    discounts = detect_isolated_clusters(attestations)
    
    # All users should have discount factors
    assert "alice" in discounts
    assert "bob" in discounts
    assert "carol" in discounts
    assert "dave" in discounts
    
    # Discount factors should be between 0 and 1
    for discount in discounts.values():
        assert 0 <= discount <= 1

def test_apply_time_decay():
    """Test time decay for attestations."""
    # Recent attestation
    decay_recent = apply_time_decay(0)
    # 1 year old
    decay_1year = apply_time_decay(365)
    # 2 years old
    decay_2years = apply_time_decay(730)
    
    # Older attestations should have lower weight
    assert decay_recent == 1.0
    assert decay_1year < decay_recent
    assert decay_2years < decay_1year
    assert decay_1year == pytest.approx(0.5, 0.01)  # Half-life at 365 days
