# Identity model for user authentication and verification

from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from datetime import datetime
from db.connection import Base

class UserIdentityModel(Base):
    __tablename__ = "user_identities"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    public_key = Column(String, unique=True)
    private_key_hash = Column(String)  # Store hash, not actual private key
    verified = Column(Boolean, default=False)
    reputation_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
