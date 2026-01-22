# user model
from pydantic import BaseModel
from datetime import datetime
from typing import List

class AttestationOut(BaseModel):
    id: int
    from_user: str
    to_user: str
    value: int
    context: str
    timestamp: datetime

    class Config:
        orm_mode = True

class UserReputation(BaseModel):
    user: str
    reputation: int
    attestations: List[AttestationOut]
