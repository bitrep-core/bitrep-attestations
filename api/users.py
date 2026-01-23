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
    print(">>> ENTERING /user endpoint")

    rows = (
        db.query(AttestationModel)
        .filter(AttestationModel.to_user == username)
        .all()
    )

    if not rows:
        raise HTTPException(status_code=404, detail="User not found")

    print(f">>> RAW ROWS: {len(rows)} found")

    for r in rows:
        print(f">>> ROW FIELDS: id={r.id}, from={r.from_user}, to={r.to_user}, value={r.value}, context={r.context}, timestamp={r.timestamp}")

    reputation = sum(r.value for r in rows)
    print(f">>> REPUTATION: {reputation}")

    try:
        attestation_list = [AttestationOut.model_validate(r) for r in rows]
    except Exception as e:
        print(">>> ERROR converting row:", e)
        raise HTTPException(status_code=500, detail="Error serializing attestations")

    print(">>> FINAL RESPONSE READY")

    return UserReputation(
        user=username,
        reputation=reputation,
        attestations=attestation_list,
    )
