# attestation model

from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from datetime import datetime
from db.connection import Base

class AttestationModel(Base):
    __tablename__ = "attestations"

    id = Column(Integer, primary_key=True, index=True)
    from_user = Column(String, index=True)
    to_user = Column(String, index=True)
    value = Column(Integer)
    context = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    signature = Column(Text)  # Cryptographic signature
    mutual_validation = Column(String)  # Mutual validation data (e.g., both parties signed)
    weight = Column(Float, default=1.0)  # Reputation weight of this attestation
