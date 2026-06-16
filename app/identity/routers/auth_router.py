from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.identity.models.user import User

from app.identity.schemas.user_create import UserCreate
from app.identity.schemas.user_response import UserResponse

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.identity.schemas.login_request import LoginRequest
from app.identity.schemas.token_response import TokenResponse

from app.core.dependencies import get_current_user

from app.core.dependencies import (
    get_current_user,
    require_role
)
from fastapi.security import OAuth2PasswordRequestForm

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

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email ya registrado"
        )

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        role=user.role,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )

    if not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )

    token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }
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
        require_role("ADMIN")
    )
):
    return {
        "message": "Acceso permitido",
        "user": current_user.email
    }
@router.get("/public-test")
def public_test():
    return {"ok": True}