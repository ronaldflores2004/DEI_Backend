from fastapi import FastAPI

# =====================================================
# Core
# =====================================================

from app.core.logging_config import (
    configure_logging
)

# =====================================================
# Identity
# =====================================================

from app.identity.routers.auth_router import router as auth_router
from app.identity.routers.patient_router import router as patient_router
from app.identity.routers.professional_router import (
    router as professional_router,
)

# =====================================================
# Therapy
# =====================================================

from app.therapy.routers.link_request_router import (
    router as link_request_router,
)
from app.therapy.routers.consent_router import (
    router as consent_router,
)

# =====================================================
# Entries
# =====================================================

from app.entries.routers.emotional_entry_router import (
    router as emotional_entry_router,
)

# =====================================================
# Analysis
# =====================================================


from app.analysis.routers.transcription_router import (
    router as transcription_router,
)
from app.analysis.routers.emotional_analysis_router import (
    router as emotional_analysis_router,
)

# =====================================================
# Recommendations
# =====================================================

from app.recommendations.routers.patient_recommendation_router import (
    router as patient_recommendation_router,
)

# =====================================================
# Sessions
# =====================================================

from app.sessions.routers.therapy_session_router import (
    router as therapy_session_router,
)
from app.sessions.routers.clinical_note_router import (
    router as clinical_note_router,
)

# =====================================================
# Notifications
# =====================================================

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
# Base de datos
# =====================================================
# Las migraciones son administradas por Alembic.

# =====================================================
# Aplicación FastAPI
# =====================================================

configure_logging()

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