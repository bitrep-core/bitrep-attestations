# endpoints for users

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import SessionLocal
from models.attestation import AttestationModel
from models.user import UserReputation, AttestationOut

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

    reputation = sum(r.value for r in rows)

    attestation_list = [AttestationOut.from_orm(r) for r in rows]

    return UserReputation(
        user=username,
        reputation=reputation,
        attestations=attestation_list,
    )

