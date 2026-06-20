from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User

from app.dashboard.schemas.patient_dashboard_response import (
    PatientDashboardResponse
)

from app.dashboard.schemas.professional_dashboard_response import (
    ProfessionalDashboardResponse
)

from app.dashboard.services.patient_dashboard_service import (
    get_patient_dashboard
)

from app.dashboard.services.professional_dashboard_service import (
    get_professional_dashboard
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
    current_user: User = Depends(get_current_user)
):

    return get_patient_dashboard(
        current_user.id,
        db
    )
    
@router.get(
    "/professional",
    response_model=ProfessionalDashboardResponse
)
def professional_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_professional_dashboard(
        current_user.id,
        db
    )