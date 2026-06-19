from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User

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


@router.post(
    "",
    response_model=PatientRecommendationResponse
)
def create(
    data: PatientRecommendationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return create_recommendation(
        current_user.id,
        data,
        db
    )


@router.get(
    "",
    response_model=list[PatientRecommendationResponse]
)
def list_my(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_my_recommendations(
        current_user.id,
        db
    )
    
@router.post(
    "/generate/{analysis_id}",
    response_model=PatientRecommendationResponse
)
def generate(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return generate_from_analysis(
        analysis_id,
        db
    )