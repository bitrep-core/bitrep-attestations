# endpoints for attestations

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from db.connection import SessionLocal
from models.attestation import AttestationModel
from models.user import AttestationOut, AttestationIn

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/attest", response_model=AttestationOut)
def create_attestation(att: AttestationIn, db: Session = Depends(get_db)):
    db_att = AttestationModel(
        from_user=att.from_user,
        to_user=att.to_user,
        value=att.value,
        context=att.context,
    )
    db.add(db_att)
    db.commit()
    db.refresh(db_att)
    return db_att

