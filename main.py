from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file
DATABASE_URL = "sqlite:///./bitrep.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(title="BitRep Attestations - Phase 1")


# Database model
class AttestationModel(Base):
    __tablename__ = "attestations"

    id = Column(Integer, primary_key=True, index=True)
    from_user = Column(String, index=True)
    to_user = Column(String, index=True)
    value = Column(Integer)  # +1 or -1
    context = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


# Create tables
Base.metadata.create_all(bind=engine)


# Input model
class AttestationIn(BaseModel):
    from_user: str
    to_user: str
    value: int
    context: str


# Output model
class AttestationOut(AttestationIn):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True


# Reputation response
class UserReputation(BaseModel):
    user: str
    reputation: int
    attestations: List[AttestationOut]


# DB session helper
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create attestation
@app.post("/attest", response_model=AttestationOut)
def create_attestation(att: AttestationIn):
    db = next(get_db())
    db_att = AttestationModel(
        from_user=att.from_user,
        to_user=att.to_user,
        value=att.value,
        context=att.context,
    )
    db.add(db_att)
    db.commit()
    db.refresh(db_att)
    return db_att


# Get user reputation
@app.get("/user/{username}", response_model=UserReputation)
def get_user_reputation(username: str):
    db = next(get_db())
    rows = (
        db.query(AttestationModel)
        .filter(AttestationModel.to_user == username)
        .all()
    )
    reputation = sum(r.value for r in rows)
    return UserReputation(
        user=username,
        reputation=reputation,
        attestations=rows,
    )
