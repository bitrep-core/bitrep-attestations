from fastapi import APIRouter, Depends, HTTPException
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

    if not rows:
        raise HTTPException(status_code=404, detail="User not found")

    reputation = sum(r.value for r in rows)

    try:
        attestation_list = [AttestationOut.model_validate(r) for r in rows]
    except Exception:
        raise HTTPException(status_code=500, detail="Error serializing attestations")

    return UserReputation(
        user=username,
        reputation=reputation,
        attestations=attestation_list,
    )
