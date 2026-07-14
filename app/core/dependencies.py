from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.config import settings

from app.identity.models.user import User

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.identity.models.professional_profile import (
    ProfessionalProfile
)

from app.identity.repositories.user_repository import (
    UserRepository
)

from app.identity.repositories.patient_repository import (
    PatientRepository
)

from app.identity.repositories.professional_repository import (
    ProfessionalRepository
)

from app.shared.enums.role_enum import (
    RoleEnum
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Token inválido"
    )

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = UserRepository.get_by_id(
        db=db,
        user_id=int(user_id)
    )

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Usuario desactivado"
        )

    return user


def require_role(required_role):

    def role_checker(
        current_user: User = Depends(
            get_current_user
        )
    ):

        if current_user.role != required_role:
            raise HTTPException(
                status_code=403,
                detail="Acceso denegado"
            )

        return current_user

    return role_checker


def get_current_patient_profile(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    if current_user.role != RoleEnum.PATIENT:
        raise HTTPException(
            status_code=403,
            detail="Acceso permitido solo para pacientes"
        )

    patient = PatientRepository.get_by_user_id(
        db=db,
        user_id=current_user.id
    )

    if not patient:
        raise HTTPException(
            status_code=403,
            detail="No tienes perfil de paciente"
        )

    return patient


def get_current_professional_profile(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    if current_user.role != RoleEnum.PROFESSIONAL:
        raise HTTPException(
            status_code=403,
            detail="Acceso permitido solo para profesionales"
        )

    professional = ProfessionalRepository.get_by_user_id(
        db=db,
        user_id=current_user.id
    )

    if not professional:
        raise HTTPException(
            status_code=403,
            detail="No tienes perfil profesional"
        )

    return professional