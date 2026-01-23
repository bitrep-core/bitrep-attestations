# Third-party attestation model for bootstrapping reputation

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from db.connection import Base

class ThirdPartyAttestationModel(Base):
    __tablename__ = "third_party_attestations"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    platform = Column(String, index=True)  # e.g., "github", "ebay", "linkedin"
    platform_username = Column(String)
    attestation_type = Column(String)  # e.g., "commits", "reviews", "transactions"
    value = Column(Float)
    metadata = Column(Text)  # JSON metadata about the attestation
    verified = Column(Integer, default=0)  # 0 = pending, 1 = verified, -1 = rejected
    weight = Column(Float, default=0.5)  # Platform attestations weighted lower
    timestamp = Column(DateTime, default=datetime.utcnow)
