from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class AttestationIn(BaseModel):
    from_user: str
    to_user: str
    value: int
    context: str
    signature: Optional[str] = None
    mutual_validation: Optional[str] = None

class AttestationOut(BaseModel):
    id: int
    from_user: str
    to_user: str
    value: int
    context: str
    timestamp: datetime
    signature: Optional[str] = None
    mutual_validation: Optional[str] = None
    weight: float = 1.0

    model_config = {"from_attributes": True}

class UserReputation(BaseModel):
    user: str
    reputation: float  # Weighted reputation score
    attestations: List[AttestationOut]
    
class UserIdentity(BaseModel):
    username: str
    public_key: str
    verified: bool = False
    reputation_score: float = 0.0

class UserIdentityCreate(BaseModel):
    username: str
    
class ZKProof(BaseModel):
    proof: str
    threshold: float
    verified: bool
