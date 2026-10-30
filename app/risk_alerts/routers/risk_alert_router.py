from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

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

from app.risk_alerts.schemas.risk_alert_item_response import (
    RiskAlertItemResponse,
    RiskAlertResolve
)

from app.risk_alerts.services.risk_alert_service import (
    RiskAlertService,
    RiskAlertTrackingService
)

from app.shared.enums.risk_alert_status_enum import (
    RiskAlertStatusEnum
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


def _get_professional_id(
    current_user: User,
    db: Session,
) -> int:

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

    return professional.id


# =====================================
# Bandeja de alertas HIGH / CRITICAL
# =====================================

@router.get(
    "/inbox",
    response_model=list[RiskAlertItemResponse]
)
def risk_alert_inbox(
    status: RiskAlertStatusEnum | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return RiskAlertTrackingService.get_inbox(
        professional_id=_get_professional_id(
            current_user,
            db
        ),
        status=status,
        db=db
    )


@router.patch(
    "/{alert_id}/seen",
    response_model=RiskAlertItemResponse
)
def mark_risk_alert_seen(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return RiskAlertTrackingService.mark_seen(
        alert_id=alert_id,
        professional_id=_get_professional_id(
            current_user,
            db
        ),
        db=db
    )


@router.patch(
    "/{alert_id}/resolve",
    response_model=RiskAlertItemResponse
)
def resolve_risk_alert(
    alert_id: int,
    data: RiskAlertResolve,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return RiskAlertTrackingService.resolve(
        alert_id=alert_id,
        professional_id=_get_professional_id(
            current_user,
            db
        ),
        resolution_note=data.resolution_note,
        db=db
    )
