from fastapi import FastAPI

from app.core.database import Base, engine

from app.identity.models.user import User
from app.identity.routers.auth_router import router as auth_router

from app.identity.models.patient_profile import PatientProfile

from app.identity.routers.patient_router import router as patient_router
from app.identity.models.professional_profile import ProfessionalProfile
from app.identity.routers.professional_router import (
    router as professional_router
)

from app.therapy.models.patient_professional import PatientProfessional
from app.therapy.models.link_request import LinkRequest

from app.therapy.routers.link_request_router import (
    router as link_request_router
)

from app.therapy.models.consent import Consent

from app.therapy.routers.consent_router import (
    router as consent_router
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DEI API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(patient_router)
app.include_router(professional_router)
app.include_router(link_request_router)
app.include_router(consent_router)
@app.get("/")
def root():
    return {
        "message": "DEI funcionando correctamente"
    }
