# user model
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from db.connection import get_db
from models.user import AttestationModel  # adjust if needed

router = APIRouter()

class AttestationOut(BaseModel):
    id: int
    from_user: str
    to_user: str
    value: int
    context: str
    timestamp: datetime

    class Config:
        from_attributes = True

class UserReputation(BaseModel):
    user: str
    reputation: int
    attestations: List[AttestationOut]

@router.get("/user/{username}", response_model=UserReputation)
def get_user_reputation(username: str, db: Session = get_db()):
    rows = db.query(AttestationModel).filter(
        (AttestationModel.from_user == username) |
        (AttestationModel.to_user == username)
    ).all()

    if not rows:
        raise HTTPException(status_code=404, detail="User not found")

    reputation = sum(row.value if row.to_user == username else -row.value for row in rows)

    return UserReputation(
        user=username,
        reputation=reputation,
        attestations=[AttestationOut.model_validate(row) for row in rows]
    )
