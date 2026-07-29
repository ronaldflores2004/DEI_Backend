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

from app.identity.schemas.user_response import (
    UserResponse
)

from app.identity.schemas.professional_profile_response import (
    ProfessionalProfileResponse
)

from app.administration.schemas.admin_dashboard_response import (
    AdminDashboardResponse
)

from app.administration.schemas.system_statistics_response import (
    SystemStatisticsResponse
)

from app.administration.schemas.user_status_response import (
    UserStatusResponse
)

from app.administration.schemas.professional_verification_response import (
    ProfessionalVerificationResponse
)

from app.administration.services.administration_service import (
    get_admin_dashboard,
    get_system_statistics,
    get_users,
    activate_user,
    deactivate_user,
    get_professionals,
    verify_professional
)

router = APIRouter(
    prefix="/admin",
    tags=["Administration"]
)


# =====================================================
# Dashboard
# =====================================================

@router.get(
    "/dashboard",
    response_model=AdminDashboardResponse
)
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(RoleEnum.ADMIN)
    )
):

    return get_admin_dashboard(db)


# =====================================================
# Estadísticas
# =====================================================

@router.get(
    "/statistics",
    response_model=SystemStatisticsResponse
)
def statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(RoleEnum.ADMIN)
    )
):

    return get_system_statistics(db)


# =====================================================
# Usuarios
# =====================================================

@router.get(
    "/users",
    response_model=list[UserResponse]
)
def users(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(RoleEnum.ADMIN)
    )
):

    return get_users(db)


# =====================================================
# Activar usuario
# =====================================================

@router.patch(
    "/users/{user_id}/activate",
    response_model=UserStatusResponse
)
def activate(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(RoleEnum.ADMIN)
    )
):

    return activate_user(
        user_id=user_id,
        db=db
    )


# =====================================================
# Desactivar usuario
# =====================================================

@router.patch(
    "/users/{user_id}/deactivate",
    response_model=UserStatusResponse
)
def deactivate(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(RoleEnum.ADMIN)
    )
):

    return deactivate_user(
        user_id=user_id,
        current_admin_id=current_user.id,
        db=db
    )


# =====================================================
# Profesionales
# =====================================================

@router.get(
    "/professionals",
    response_model=list[
        ProfessionalProfileResponse
    ]
)
def professionals(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(RoleEnum.ADMIN)
    )
):

    return get_professionals(db)


# =====================================================
# Verificar profesional
# =====================================================

@router.patch(
    "/professionals/{professional_id}/verify",
    response_model=ProfessionalVerificationResponse
)
def verify(
    professional_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(RoleEnum.ADMIN)
    )
):

    return verify_professional(
        professional_id=professional_id,
        db=db
    )