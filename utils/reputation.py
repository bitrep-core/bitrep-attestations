# reputation calculation - Modified PageRank algorithm for weighted reputation

from typing import Dict, List, Tuple
import math

def calculate_weighted_reputation(attestations: List[Tuple[str, str, int, float]]) -> Dict[str, float]:
    """
    Calculate weighted reputation using modified PageRank algorithm.
    
    Args:
        attestations: List of (from_user, to_user, value, weight) tuples
        
    Returns:
        Dictionary mapping username to reputation score
    """
    # Build graph
    users = set()
    incoming = {}  # user -> list of (from_user, value, weight)
    outgoing = {}  # user -> list of to_user
    
    for from_user, to_user, value, weight in attestations:
        users.add(from_user)
        users.add(to_user)
        
        if to_user not in incoming:
            incoming[to_user] = []
        incoming[to_user].append((from_user, value, weight))
        
        if from_user not in outgoing:
            outgoing[from_user] = []
        outgoing[from_user].append(to_user)
    
    # Initialize reputation scores
    reputation = {user: 1.0 for user in users}
    
    # PageRank parameters
    damping_factor = 0.85
    iterations = 20
    
    # Iterative calculation
    for _ in range(iterations):
        new_reputation = {}
        
        for user in users:
            # Base reputation (like PageRank's random jump)
            score = (1 - damping_factor)
            
            # Add weighted reputation from incoming attestations
            if user in incoming:
                for from_user, value, weight in incoming[user]:
                    # Weight by attester's reputation and attestation value
                    out_count = len(outgoing.get(from_user, []))
                    if out_count > 0:
                        contribution = (reputation[from_user] / out_count) * value * weight
                        score += damping_factor * contribution
            
            new_reputation[user] = max(0, score)  # Ensure non-negative
        
        reputation = new_reputation
    
    return reputation

def calculate_attestation_weight(attester_reputation: float, cluster_discount: float = 1.0) -> float:
    """
    Calculate the weight of an attestation based on attester's reputation.
    
    Args:
        attester_reputation: Current reputation score of the attester
        cluster_discount: Discount factor for isolated clusters (0-1)
        
    Returns:
        Weight value for the attestation
    """
    # Logarithmic scaling to prevent extreme weights
    base_weight = math.log(1 + attester_reputation) / math.log(2)
    return base_weight * cluster_discount

def detect_isolated_clusters(attestations: List[Tuple[str, str, int, float]], threshold: float = 0.3) -> Dict[str, float]:
    """
    Detect isolated clusters of mutual attestation (Sybil resistance).
    
    Returns:
        Dictionary mapping username to discount factor (0-1)
    """
    # Build graph
    users = set()
    edges = {}
    
    for from_user, to_user, _, _ in attestations:
        users.add(from_user)
        users.add(to_user)
        
        if from_user not in edges:
            edges[from_user] = set()
        edges[from_user].add(to_user)
    
    # Handle edge cases
    if len(users) == 0:
        return {}
    if len(users) == 1:
        return {list(users)[0]: 1.0}
    
    # Calculate connectivity to broader network
    discounts = {}
    for user in users:
        # Count connections outside immediate neighbors
        immediate = edges.get(user, set())
        
        # Count second-degree connections
        extended = set()
        for neighbor in immediate:
            extended.update(edges.get(neighbor, set()))
        extended -= immediate
        extended.discard(user)
        
        # Discount if mostly isolated
        # Avoid division by zero
        total_possible = len(users) - len(immediate) - 1
        if total_possible <= 0:
            connectivity = 1.0
        else:
            connectivity = len(extended) / total_possible
        
        discounts[user] = min(1.0, threshold + connectivity)
    
    return discounts

def apply_time_decay(attestation_age_days: int, half_life_days: int = 365) -> float:
    """
    Apply time decay to attestation weight.
    
    Args:
        attestation_age_days: Age of attestation in days
        half_life_days: Half-life for reputation decay
        
    Returns:
        Decay factor (0-1)
    """
    return math.exp(-attestation_age_days * math.log(2) / half_life_days)

