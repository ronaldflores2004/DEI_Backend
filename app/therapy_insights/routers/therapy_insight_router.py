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
    generate_insights
)

from app.therapy.services.access_policy_service import (
    has_active_consent
)

from app.identity.repositories.professional_repository import (
    ProfessionalRepository
)

from app.therapy.repositories.patient_professional_repository import (
    PatientProfessionalRepository
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

    relation = (
        PatientProfessionalRepository.get_active_relation(
            db=db,
            patient_id=patient_id,
            professional_id=professional.id
        )
    )

    if not relation:
        raise HTTPException(
            status_code=403,
            detail="No tienes acceso a este paciente"
        )

    # Seguridad clínica:
    # además de la relación terapéutica,
    # debe existir consentimiento activo.

    if not has_active_consent(
        patient_id=patient_id,
        professional_id=professional.id,
        db=db
    ):
        raise HTTPException(
            status_code=403,
            detail="No existe consentimiento activo"
        )

    return generate_insights(
        patient_id,
        db
    )