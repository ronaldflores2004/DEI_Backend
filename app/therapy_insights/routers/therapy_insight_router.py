from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User

from app.identity.models.professional_profile import (
    ProfessionalProfile
)

from app.therapy.models.patient_professional import (
    PatientProfessional
)

from app.therapy_insights.schemas.therapy_insight_response import (
    TherapyInsightResponse
)

from app.therapy_insights.services.insight_generator_service import (
    generate_insights
)

from app.therapy.services.access_policy_service import (
    has_active_consent
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
        db.query(ProfessionalProfile)
        .filter(
            ProfessionalProfile.user_id == current_user.id
        )
        .first()
    )

    if not professional:
        raise HTTPException(
            status_code=403,
            detail="No tienes perfil profesional"
        )

    relation = (
        db.query(PatientProfessional)
        .filter(
            PatientProfessional.patient_id == patient_id,
            PatientProfessional.professional_id == professional.id,
            PatientProfessional.active == True
        )
        .first()
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