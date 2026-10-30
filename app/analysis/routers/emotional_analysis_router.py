from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_patient_profile
)

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.analysis.schemas.emotional_analysis_create import (
    EmotionalAnalysisCreate
)

from app.analysis.schemas.emotional_analysis_response import (
    EmotionalAnalysisResponse
)

from app.analysis.schemas.crisis_support_response import (
    CrisisSupportResponse
)

from app.analysis.schemas.weekly_summary_response import (
    WeeklySummaryResponse
)

from app.analysis.services.emotional_analysis_service import (
    EmotionalAnalysisService
)

from app.analysis.services.weekly_summary_service import (
    WeeklySummaryService,
)

from app.risk_alerts.services.crisis_response_service import (
    CrisisResponseService
)

router = APIRouter(
    prefix="/analysis",
    tags=["Emotional Analysis"]
)


def _with_crisis_support(
    analysis,
    patient: PatientProfile,
    db: Session,
) -> EmotionalAnalysisResponse:
    """
    Agrega ayuda inmediata y avisa al profesional
    cuando el análisis resulta HIGH o CRITICAL.
    """

    response = EmotionalAnalysisResponse.model_validate(
        analysis
    )

    crisis_support = CrisisResponseService.handle(
        analysis=analysis,
        patient=patient,
        db=db
    )

    if crisis_support:
        response.crisis_support = (
            CrisisSupportResponse.model_validate(
                crisis_support
            )
        )

    return response


# =====================================
# Crear análisis manual
# =====================================

@router.post(
    "/entries/{entry_id}",
    response_model=EmotionalAnalysisResponse
)
def create_analysis(
    entry_id: int,
    data: EmotionalAnalysisCreate,
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    analysis = EmotionalAnalysisService.create_analysis(
        entry_id=entry_id,
        patient=patient,
        data=data,
        db=db
    )

    return _with_crisis_support(
        analysis=analysis,
        patient=patient,
        db=db
    )


# =====================================
# Obtener análisis
# =====================================

@router.get(
    "/entries/{entry_id}",
    response_model=EmotionalAnalysisResponse
)
def get_analysis(
    entry_id: int,
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    return EmotionalAnalysisService.get_analysis(
        entry_id=entry_id,
        patient=patient,
        db=db
    )


# =====================================
# Análisis automático IA
# =====================================

@router.post(
    "/entries/{entry_id}/auto",
    response_model=EmotionalAnalysisResponse
)
def auto_analyze(
    entry_id: int,
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    analysis = EmotionalAnalysisService.create_analysis_from_entry(
        entry_id=entry_id,
        patient=patient,
        db=db
    )

    return _with_crisis_support(
        analysis=analysis,
        patient=patient,
        db=db
    )

# =====================================
# Reanalizar entrada con IA
# =====================================

@router.post(
    "/entries/{entry_id}/reanalyze",
    response_model=EmotionalAnalysisResponse
)
def reanalyze(
    entry_id: int,
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    analysis = EmotionalAnalysisService.create_analysis_from_entry(
        entry_id=entry_id,
        patient=patient,
        db=db
    )

    return _with_crisis_support(
        analysis=analysis,
        patient=patient,
        db=db
    )

# =====================================
# Resumen semanal
# =====================================

@router.get(
    "/weekly-summary",
    response_model=WeeklySummaryResponse
)
def weekly_summary(
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    return WeeklySummaryService.get_weekly_summary(
        patient=patient,
        db=db
    )