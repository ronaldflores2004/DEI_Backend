from fastapi import FastAPI

# =====================================================
# Core
# =====================================================

from app.core.database import Base, engine

# =====================================================
# Identity
# =====================================================

from app.identity.models.user import User
from app.identity.models.patient_profile import PatientProfile
from app.identity.models.professional_profile import ProfessionalProfile

from app.identity.routers.auth_router import router as auth_router
from app.identity.routers.patient_router import router as patient_router
from app.identity.routers.professional_router import (
    router as professional_router,
)

# =====================================================
# Therapy
# =====================================================

from app.therapy.models.patient_professional import PatientProfessional
from app.therapy.models.link_request import LinkRequest
from app.therapy.models.consent import Consent

from app.therapy.routers.link_request_router import (
    router as link_request_router,
)
from app.therapy.routers.consent_router import (
    router as consent_router,
)

# =====================================================
# Entries
# =====================================================

from app.entries.models.emotional_entry import EmotionalEntry

from app.entries.routers.emotional_entry_router import (
    router as emotional_entry_router,
)
from app.entries.routers.audio_router import (
    router as audio_router,
)

# =====================================================
# Analysis
# =====================================================

from app.analysis.models.audio_transcription import (
    AudioTranscription,
)
from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis,
)

from app.analysis.routers.transcription_router import (
    router as transcription_router,
)
from app.analysis.routers.emotional_analysis_router import (
    router as emotional_analysis_router,
)

# =====================================================
# Recommendations
# =====================================================

from app.recommendations.models.patient_recommendation import (
    PatientRecommendation,
)

from app.recommendations.routers.patient_recommendation_router import (
    router as patient_recommendation_router,
)

# =====================================================
# Sessions
# =====================================================

from app.sessions.models.therapy_session import (
    TherapySession,
)
from app.sessions.models.clinical_note import (
    ClinicalNote,
)

from app.sessions.routers.therapy_session_router import (
    router as therapy_session_router,
)
from app.sessions.routers.clinical_note_router import (
    router as clinical_note_router,
)

# =====================================================
# Notifications
# =====================================================

from app.notifications.models.notification import (
    Notification,
)

from app.notifications.routers.notification_router import (
    router as notification_router,
)

# =====================================================
# Dashboard
# =====================================================

from app.dashboard.routers.dashboard_router import (
    router as dashboard_router,
)

# =====================================================
# Therapy Insights
# =====================================================

from app.therapy_insights.routers.therapy_insight_router import (
    router as therapy_insight_router,
)

# =====================================================
# Risk Alerts
# =====================================================

from app.risk_alerts.routers.risk_alert_router import (
    router as risk_alert_router,
)

# =====================================================
# Administration
# =====================================================

from app.administration.routers.administration_router import (
    router as administration_router,
)

# =====================================================
# Crear tablas (Temporal)
# TODO: Reemplazar por Alembic en producción.
# =====================================================

Base.metadata.create_all(bind=engine)

# =====================================================
# Aplicación FastAPI
# =====================================================

app = FastAPI(
    title="DEI API",
    version="1.0.0",
)

# =====================================================
# Routers
# =====================================================

app.include_router(auth_router)
app.include_router(patient_router)
app.include_router(professional_router)

app.include_router(link_request_router)
app.include_router(consent_router)

app.include_router(emotional_entry_router)
app.include_router(audio_router)

app.include_router(transcription_router)
app.include_router(emotional_analysis_router)

app.include_router(patient_recommendation_router)

app.include_router(therapy_session_router)
app.include_router(clinical_note_router)

app.include_router(notification_router)

app.include_router(dashboard_router)

app.include_router(therapy_insight_router)

app.include_router(risk_alert_router)

app.include_router(administration_router)

# =====================================================
# Root
# =====================================================

@app.get("/")
def root():
    return {
        "message": "DEI funcionando correctamente"
    }