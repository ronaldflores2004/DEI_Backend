from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.dashboard.schemas.patient_dashboard_response import (
    PatientDashboardResponse
)

from app.dashboard.schemas.professional_dashboard_response import (
    ProfessionalDashboardResponse
)

from app.dashboard.services.patient_dashboard_service import (
    PatientDashboardService
)

from app.dashboard.services.professional_dashboard_service import (
    ProfessionalDashboardService
)

from app.core.dependencies import (
    get_current_patient_profile, get_current_professional_profile
)

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.identity.models.professional_profile import (
    ProfessionalProfile
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/patient",
    response_model=PatientDashboardResponse
)
def patient_dashboard(
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    return PatientDashboardService.get_dashboard(
        patient=patient,
        db=db
    )
    
@router.get(
    "/professional",
    response_model=ProfessionalDashboardResponse
)
def professional_dashboard(
    db: Session = Depends(get_db),
    professional: ProfessionalProfile = Depends(
        get_current_professional_profile
    )
):

    return ProfessionalDashboardService.get_dashboard(
        professional=professional,
        db=db
    )