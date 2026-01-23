from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connection import SessionLocal
from models.attestation import AttestationModel
from models.identity import UserIdentityModel
from models.user import UserReputation, AttestationOut
from utils.reputation import calculate_weighted_reputation
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/user/{username}", response_model=UserReputation)
def get_user_reputation(username: str, db: Session = Depends(get_db)):
    rows = (
        db.query(AttestationModel)
        .filter(AttestationModel.to_user == username)
        .all()
    )

    if not rows:
        raise HTTPException(status_code=404, detail="User not found")

    # Get all attestations for weighted calculation
    all_attestations = db.query(AttestationModel).all()
    
    # Prepare data for weighted reputation calculation
    attestation_data = [
        (att.from_user, att.to_user, att.value, att.weight)
        for att in all_attestations
    ]
    
    # Calculate weighted reputation using PageRank algorithm
    if attestation_data:
        reputation_scores = calculate_weighted_reputation(attestation_data)
        reputation = reputation_scores.get(username, 0.0)
    else:
        reputation = sum(r.value for r in rows)

    # Update user identity with new reputation score
    identity = db.query(UserIdentityModel).filter(
        UserIdentityModel.username == username
    ).first()
    
    if identity:
        identity.reputation_score = reputation
        db.commit()

    try:
        attestation_list = [AttestationOut.model_validate(r) for r in rows]
    except Exception:
        raise HTTPException(status_code=500, detail="Error serializing attestations")

    return UserReputation(
        user=username,
        reputation=reputation,
        attestations=attestation_list,
    )
