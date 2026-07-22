from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User

from app.notifications.schemas.notification_response import (
    NotificationResponse
)

from app.notifications.schemas.notification_read_response import (
    NotificationReadResponse
)

from app.notifications.services.notification_service import (
    NotificationService
)

from app.notifications.schemas.notification_summary_response import (
    NotificationSummaryResponse
)



router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.get(
    "",
    response_model=list[NotificationResponse]
)
def list_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return NotificationService.get_notifications(
        current_user.id,
        db
    )


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationReadResponse
)
def read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return NotificationService.mark_as_read(
        notification_id,
        current_user.id,
        db
    )
    
@router.get(
    "/summary",
    response_model=NotificationSummaryResponse
)
def notification_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return NotificationService.get_notification_summary(
        current_user.id,
        db
    )