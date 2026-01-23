from pydantic import BaseModel
from datetime import datetime
from typing import List

class AttestationIn(BaseModel):
    from_user: str
    to_user: str
    value: int
    context: str

class AttestationOut(BaseModel):
    id: int
    from_user: str
    to_user: str
    value: int
    context: str
    timestamp: datetime

    model_config = {"from_attributes": True}

class UserReputation(BaseModel):
    user: str
    reputation: int
    attestations: List[AttestationOut]
