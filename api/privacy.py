# API endpoints for privacy features and zero-knowledge proofs

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connection import SessionLocal
from models.identity import UserIdentityModel
from models.attestation import AttestationModel
from models.user import ZKProof
from utils.zkproof import generate_zk_proof, verify_zk_proof, create_selective_disclosure_proof
from pydantic import BaseModel
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ThresholdProofRequest(BaseModel):
    username: str
    threshold: float

class SelectiveDisclosureRequest(BaseModel):
    username: str
    selected_indices: List[int]

@router.post("/privacy/prove-threshold", response_model=ZKProof)
def prove_reputation_threshold(request: ThresholdProofRequest, db: Session = Depends(get_db)):
    """
    Generate a zero-knowledge proof that user's reputation exceeds a threshold.
    Does not reveal exact reputation score.
    """
    # Get user's reputation
    identity = db.query(UserIdentityModel).filter(
        UserIdentityModel.username == request.username
    ).first()
    
    if not identity:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate ZK proof
    proof_string, meets_threshold = generate_zk_proof(
        identity.reputation_score,
        request.threshold
    )
    
    return ZKProof(
        proof=proof_string,
        threshold=request.threshold,
        verified=meets_threshold
    )

@router.post("/privacy/verify-threshold")
def verify_reputation_threshold(proof_data: ZKProof):
    """
    Verify a zero-knowledge proof without learning the actual reputation.
    """
    is_valid = verify_zk_proof(
        proof_data.proof,
        proof_data.threshold,
        proof_data.verified
    )
    
    return {
        "valid": is_valid,
        "threshold": proof_data.threshold,
        "meets_threshold": proof_data.verified if is_valid else None
    }

@router.post("/privacy/selective-disclosure")
def create_selective_disclosure(request: SelectiveDisclosureRequest, db: Session = Depends(get_db)):
    """
    Create a selective disclosure proof for specific attestations.
    Allows proving certain attestations exist without revealing all.
    """
    # Get all user attestations
    attestations = db.query(AttestationModel).filter(
        AttestationModel.to_user == request.username
    ).all()
    
    if not attestations:
        raise HTTPException(status_code=404, detail="No attestations found")
    
    # Convert to list of dicts
    attestation_list = []
    for att in attestations:
        attestation_list.append({
            "id": att.id,
            "from_user": att.from_user,
            "to_user": att.to_user,
            "value": att.value,
            "context": att.context,
            "timestamp": str(att.timestamp)
        })
    
    # Validate selected indices
    if any(i < 0 or i >= len(attestation_list) for i in request.selected_indices):
        raise HTTPException(status_code=400, detail="Invalid attestation indices")
    
    # Create selective disclosure proof
    disclosure_proof = create_selective_disclosure_proof(
        attestation_list,
        request.selected_indices
    )
    
    return {
        "username": request.username,
        "proof": disclosure_proof,
        "message": "Selective disclosure proof created"
    }

@router.get("/privacy/reputation-bands/{username}")
def get_reputation_band(username: str, db: Session = Depends(get_db)):
    """
    Return reputation in broad bands instead of exact score for privacy.
    E.g., "0-10", "10-50", "50-100", "100-500", "500+"
    """
    identity = db.query(UserIdentityModel).filter(
        UserIdentityModel.username == username
    ).first()
    
    if not identity:
        raise HTTPException(status_code=404, detail="User not found")
    
    reputation = identity.reputation_score
    
    # Define reputation bands
    if reputation < 10:
        band = "0-10"
    elif reputation < 50:
        band = "10-50"
    elif reputation < 100:
        band = "50-100"
    elif reputation < 500:
        band = "100-500"
    else:
        band = "500+"
    
    return {
        "username": username,
        "reputation_band": band,
        "message": "Reputation shown in bands for privacy"
    }
