from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_patient_profile,
    get_current_professional_profile
)

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.recommendations.schemas.patient_recommendation_create import (
    PatientRecommendationCreate
)

from app.recommendations.schemas.patient_recommendation_response import (
    PatientRecommendationResponse,
    RecommendationReviewResponse
)

from app.recommendations.schemas.recommendation_review import (
    RecommendationApprove
)

from app.identity.models.professional_profile import (
    ProfessionalProfile
)

from app.shared.enums.recommendation_status_enum import (
    RecommendationStatusEnum
)

from app.recommendations.services.patient_recommendation_service import (
    PatientRecommendationService
)


from app.platform_consents.dependencies import (
    require_ai_consent
)

router = APIRouter(
    prefix="/recommendations",
    tags=["Patient Recommendations"]
)


# =====================================
# Crear recomendación manual
# =====================================

@router.post(
    "/analysis/{analysis_id}",
    response_model=PatientRecommendationResponse
)
def create(
    analysis_id: int,
    data: PatientRecommendationCreate,
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    return PatientRecommendationService.create_recommendation(
        analysis_id=analysis_id,
        patient=patient,
        data=data,
        db=db
    )


# =====================================
# Listar recomendaciones del paciente
# =====================================

@router.get(
    "",
    response_model=list[PatientRecommendationResponse]
)
def list_my(
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    return PatientRecommendationService.get_my_recommendations(
        patient=patient,
        db=db
    )


# =====================================
# Generar recomendación desde análisis
# =====================================

@router.post(
    "/generate/{analysis_id}",
    response_model=PatientRecommendationResponse,
    dependencies=[Depends(require_ai_consent)]
)
def generate(
    analysis_id: int,
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    recommendation = PatientRecommendationService.generate_from_analysis(
        analysis_id=analysis_id,
        patient=patient,
        db=db
    )

    response = PatientRecommendationResponse.model_validate(
        recommendation
    )

    # El paciente no ve el texto hasta que el
    # profesional lo apruebe.
    if response.status != RecommendationStatusEnum.APPROVED:
        response.content = None

    return response


# =====================================
# Revisión por el profesional
# =====================================

@router.get(
    "/review/pending",
    response_model=list[RecommendationReviewResponse]
)
def list_pending_reviews(
    db: Session = Depends(get_db),
    professional: ProfessionalProfile = Depends(
        get_current_professional_profile
    )
):

    return PatientRecommendationService.get_pending_reviews(
        professional=professional,
        db=db
    )


@router.patch(
    "/review/{recommendation_id}/approve",
    response_model=RecommendationReviewResponse
)
def approve_recommendation(
    recommendation_id: int,
    data: RecommendationApprove,
    db: Session = Depends(get_db),
    professional: ProfessionalProfile = Depends(
        get_current_professional_profile
    )
):

    return PatientRecommendationService.review(
        recommendation_id=recommendation_id,
        professional=professional,
        approve=True,
        title=data.title,
        content=data.content,
        db=db
    )


@router.patch(
    "/review/{recommendation_id}/reject",
    response_model=RecommendationReviewResponse
)
def reject_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
    professional: ProfessionalProfile = Depends(
        get_current_professional_profile
    )
):

    return PatientRecommendationService.review(
        recommendation_id=recommendation_id,
        professional=professional,
        approve=False,
        db=db
    )
