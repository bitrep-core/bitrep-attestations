# user model
from pydantic import BaseModel
from datetime import datetime
from typing import List

class AttestationIn(BaseModel):
    from_user: str
    to_user: str
    value: int
    context: str

class AttestationOut(AttestationIn):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class UserReputation(BaseModel):
    user: str
    reputation: int
    attestations: List[AttestationOut]

