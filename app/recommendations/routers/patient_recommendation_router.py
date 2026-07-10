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

from app.recommendations.schemas.patient_recommendation_create import (
    PatientRecommendationCreate
)

from app.recommendations.schemas.patient_recommendation_response import (
    PatientRecommendationResponse
)

from app.recommendations.services.patient_recommendation_service import (
    create_recommendation,
    get_my_recommendations
)

from app.recommendations.services.patient_recommendation_generator_service import (
    generate_from_analysis
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

    return create_recommendation(
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

    return get_my_recommendations(
        patient=patient,
        db=db
    )


# =====================================
# Generar recomendación desde análisis
# =====================================

@router.post(
    "/generate/{analysis_id}",
    response_model=PatientRecommendationResponse
)
def generate(
    analysis_id: int,
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    return generate_from_analysis(
        analysis_id=analysis_id,
        patient=patient,
        db=db
    )