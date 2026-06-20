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

from app.entries.models.emotional_entry import EmotionalEntry

from app.entries.routers.emotional_entry_router import (
    router as emotional_entry_router
)

from app.entries.routers.audio_router import (
    router as audio_router
)

from app.analysis.models.audio_transcription import (
    AudioTranscription
)

from app.analysis.routers.transcription_router import (
    router as transcription_router
)
from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis
)
from app.analysis.routers.gemini_router import (
    router as gemini_router
)
from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis
)
from app.analysis.routers.emotional_analysis_router import (
    router as emotional_analysis_router
)

from app.recommendations.models.patient_recommendation import (
    PatientRecommendation
)

from app.recommendations.routers.patient_recommendation_router import (
    router as patient_recommendation_router
)

from app.dashboard.routers.dashboard_router import (
    router as dashboard_router
)

from app.therapy_insights.routers.therapy_insight_router import (
    router as therapy_insight_router
)

from app.risk_alerts.routers.risk_alert_router import (
    router as risk_alert_router
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
app.include_router(emotional_entry_router)
app.include_router(audio_router)
app.include_router(transcription_router)
app.include_router(gemini_router)
app.include_router(emotional_analysis_router)
app.include_router(
    patient_recommendation_router
)
app.include_router(dashboard_router)
app.include_router(
    therapy_insight_router
)

app.include_router(
    risk_alert_router
)

@app.get("/")
def root():
    return {
        "message": "DEI funcionando correctamente"
    }
