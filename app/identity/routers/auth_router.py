from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.identity.models.user import User



from app.identity.schemas.user_create import UserCreate
from app.identity.schemas.user_response import UserResponse
from app.identity.schemas.token_response import TokenResponse

from app.identity.services.auth_service import (
    AuthService
)

from app.core.dependencies import (
    get_current_user,
    require_role
)

from app.shared.enums.role_enum import RoleEnum

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



@router.post(
    "/register",
    response_model=UserResponse
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    return AuthService.register_user(
        db=db,
        user_data=user
    )


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    token = AuthService.authenticate(
        db=db,
        email=form_data.username,
        password=form_data.password
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer"
    )


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active
    }


@router.get("/test-me")
def test_me(
    current_user: User = Depends(get_current_user)
):
    return current_user.email


@router.get("/admin-only")
def admin_only(
    current_user: User = Depends(
        require_role(RoleEnum.ADMIN)
    )
):
    return {
        "message": "Acceso permitido",
        "user": current_user.email
    }


@router.get("/public-test")
def public_test():
    return {
        "ok": True
    }