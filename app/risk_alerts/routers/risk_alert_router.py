from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User

from app.identity.repositories.professional_repository import (
    ProfessionalRepository
)

from app.risk_alerts.schemas.risk_alert_response import (
    RiskAlertResponse
)

from app.risk_alerts.services.risk_alert_service import (
    RiskAlertService
)

router = APIRouter(
    prefix="/risk-alerts",
    tags=["Risk Alerts"]
)


@router.get(
    "",
    response_model=list[RiskAlertResponse]
)
def risk_alerts(
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
        return []

    return RiskAlertService.get_risk_alerts(
        professional.id,
        db
    )