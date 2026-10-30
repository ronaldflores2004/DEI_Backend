from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    require_role
)

from app.shared.enums.role_enum import (
    RoleEnum
)

from app.identity.models.user import User

from app.administration.schemas.ai_settings_schemas import (
    AISettingsResponse,
    AISettingsUpdate
)

from app.administration.schemas.crisis_line_schemas import (
    CrisisLineCreate,
    CrisisLineResponse,
    CrisisLineUpdate
)

from app.administration.services.admin_settings_service import (
    AdminSettingsService
)

router = APIRouter(
    prefix="/admin",
    tags=["Administration"]
)

require_admin = require_role(RoleEnum.ADMIN)


# =====================================================
# Líneas de crisis
# =====================================================

@router.get(
    "/crisis-lines",
    response_model=list[CrisisLineResponse]
)
def list_crisis_lines(
    country_code: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    return AdminSettingsService.list_crisis_lines(
        db=db,
        country_code=country_code
    )


@router.post(
    "/crisis-lines",
    response_model=CrisisLineResponse
)
def create_crisis_line(
    data: CrisisLineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    return AdminSettingsService.create_crisis_line(
        data=data,
        db=db
    )


@router.patch(
    "/crisis-lines/{line_id}",
    response_model=CrisisLineResponse
)
def update_crisis_line(
    line_id: int,
    data: CrisisLineUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    return AdminSettingsService.update_crisis_line(
        line_id=line_id,
        data=data,
        db=db
    )


# =====================================================
# Proveedor de IA
# =====================================================

@router.get(
    "/ai-settings",
    response_model=AISettingsResponse
)
def get_ai_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    return AdminSettingsService.get_ai_settings(db)


@router.put(
    "/ai-settings",
    response_model=AISettingsResponse
)
def update_ai_settings(
    data: AISettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    return AdminSettingsService.update_ai_settings(
        provider_chain=data.provider_chain,
        current_user=current_user,
        db=db
    )


@router.delete(
    "/ai-settings",
    response_model=AISettingsResponse
)
def reset_ai_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    return AdminSettingsService.reset_ai_settings(db)
