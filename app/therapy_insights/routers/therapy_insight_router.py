from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User

from app.therapy_insights.schemas.therapy_insight_response import (
    TherapyInsightResponse
)

from app.therapy_insights.services.insight_generator_service import (
    TherapyInsightService
)

from app.therapy.services.access_policy_service import (
    AccessPolicyService
)

from app.identity.repositories.professional_repository import (
    ProfessionalRepository
)



router = APIRouter(
    prefix="/therapy-insights",
    tags=["Therapy Insights"]
)


@router.get(
    "/patient/{patient_id}",
    response_model=list[TherapyInsightResponse]
)
def get_patient_insights(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    professional = (
        ProfessionalRepository.get_by_user_id(
            db=db,
            user_id=current_user.id
        )
    )

    if not professional:
        raise HTTPException(
            status_code=403,
            detail="No tienes perfil profesional"
        )

    AccessPolicyService.require_patient_access(
        patient_id=patient_id,
        professional_id=professional.id,
        db=db
    )

    return TherapyInsightService.generate_insights(
        patient_id=patient_id,
        db=db
    )