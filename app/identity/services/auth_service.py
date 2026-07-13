from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)

from app.identity.models.user import User
from app.identity.repositories.user_repository import (
    UserRepository,
)

from app.identity.schemas.user_create import UserCreate

from app.shared.enums.role_enum import RoleEnum


class AuthService:
    """
    Servicio encargado de la autenticación y
    registro de usuarios.
    """

    @staticmethod
    def register_user(
        db: Session,
        user_data: UserCreate,
    ) -> User:

        if UserRepository.exists_email(
            db,
            user_data.email,
        ):
            raise HTTPException(
                status_code=400,
                detail="Email ya registrado",
            )

        if user_data.role == RoleEnum.ADMIN:
            raise HTTPException(
                status_code=403,
                detail="No está permitido registrar administradores",
            )

        user = User(
            email=user_data.email,
            password_hash=hash_password(
                user_data.password
            ),
            role=user_data.role,
            is_active=True,
        )

        return UserRepository.create(
            db,
            user,
        )

    @staticmethod
    def authenticate(
        db: Session,
        email: str,
        password: str,
    ) -> str:

        user = UserRepository.get_by_email(
            db,
            email,
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Credenciales inválidas",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=403,
                detail="Usuario desactivado",
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=401,
                detail="Credenciales inválidas",
            )

        return create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": user.role,
            }
        )