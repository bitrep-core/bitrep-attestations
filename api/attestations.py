# endpoints for attestations

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from db.connection import SessionLocal
from models.attestation import AttestationModel
from models.user import AttestationOut, AttestationIn
from models.identity import UserIdentityModel
from utils.crypto import sign_attestation, verify_signature
from utils.reputation import calculate_attestation_weight

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/attest", response_model=AttestationOut)
def create_attestation(att: AttestationIn, db: Session = Depends(get_db)):
    # Get attester's reputation for weight calculation
    attester = db.query(UserIdentityModel).filter(
        UserIdentityModel.username == att.from_user
    ).first()
    
    # Calculate weight based on attester's reputation
    attester_reputation = attester.reputation_score if attester else 1.0
    weight = calculate_attestation_weight(attester_reputation)
    
    db_att = AttestationModel(
        from_user=att.from_user,
        to_user=att.to_user,
        value=att.value,
        context=att.context,
        signature=att.signature,
        mutual_validation=att.mutual_validation,
        weight=weight
    )
    db.add(db_att)
    db.commit()
    db.refresh(db_att)
    return db_att

