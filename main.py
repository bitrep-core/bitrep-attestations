from fastapi import FastAPI
from db.connection import Base, engine
from api.attestations import router as attest_router
from api.users import router as users_router
from models.attestation import AttestationModel

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BitRep Attestations - Modular")

app.include_router(attest_router)
app.include_router(users_router)
