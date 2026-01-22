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
    print(">>> ENTERING /user endpoint")

    rows = (
        db.query(AttestationModel)
        .filter(AttestationModel.to_user == username)
        .all()
    )

    print(">>> RAW ROWS:", rows)

    for r in rows:
        print(">>> ROW FIELDS:", r.id, r.from_user, r.to_user, r.value, r.context, r.timestamp)

    reputation = sum(r.value for r in rows)
    print(">>> REPUTATION:", reputation)

    attestation_list = []
    for r in rows:
        try:
            converted = AttestationOut.from_orm(r)
            attestation_list.append(converted)
        except Exception as e:
            print(">>> ERROR converting row:", e)
            raise e

    print(">>> FINAL RESPONSE READY")

    return UserReputation(
        user=username,
        reputation=reputation,
        attestations=attestation_list,
    )
