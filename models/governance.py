# Governance models for proposals and voting

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum as SQLEnum
from datetime import datetime
from db.connection import Base
import enum

class ProposalStatus(str, enum.Enum):
    ACTIVE = "active"
    PASSED = "passed"
    REJECTED = "rejected"
    EXPIRED = "expired"

class GovernanceProposalModel(Base):
    __tablename__ = "governance_proposals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    proposer = Column(String, index=True)
    status = Column(SQLEnum(ProposalStatus), default=ProposalStatus.ACTIVE)
    votes_for = Column(Float, default=0.0)
    votes_against = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

class VoteModel(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(Integer, index=True)
    voter = Column(String, index=True)
    vote_value = Column(Float)  # Weighted vote value
    support = Column(Integer)  # 1 for yes, -1 for no
    timestamp = Column(DateTime, default=datetime.utcnow)
