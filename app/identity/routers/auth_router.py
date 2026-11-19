from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.identity.models.user import User



from app.identity.schemas.user_create import UserCreate
from app.identity.schemas.user_response import UserResponse
from app.identity.schemas.token_response import TokenResponse
from app.identity.schemas.password_reset import (
    ForgotPasswordRequest,
    MessageResponse,
    ResetPasswordRequest,
    VerifyResetCodeRequest,
    VerifyResetCodeResponse,
)

from app.identity.services.auth_service import (
    AuthService
)
from app.identity.services.password_reset_service import (
    FORGOT_PASSWORD_MESSAGE,
    RESET_PASSWORD_MESSAGE,
    PasswordResetService,
)

from app.core.rate_limit import RateLimiter

from app.core.dependencies import (
    get_current_user
)



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Límites por IP. El límite por cuenta (códigos por
# hora) se aplica en el servicio, en la base de datos.
forgot_password_limiter = RateLimiter(
    name="forgot-password",
    max_requests=5,
    window_seconds=15 * 60
)

reset_code_limiter = RateLimiter(
    name="reset-code",
    max_requests=10,
    window_seconds=15 * 60
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


# =====================================
# Recuperación de contraseña
# =====================================

@router.post(
    "/forgot-password",
    response_model=MessageResponse,
    status_code=202,
    dependencies=[Depends(forgot_password_limiter)]
)
def forgot_password(
    data: ForgotPasswordRequest,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Envía un código de 6 dígitos al correo. Responde
    lo mismo exista o no la cuenta.
    """

    email = PasswordResetService.request_reset(
        db=db,
        email=data.email,
        requested_ip=(
            request.client.host
            if request.client
            else None
        )
    )

    if email is not None:
        background_tasks.add_task(email.send)

    return MessageResponse(
        message=FORGOT_PASSWORD_MESSAGE
    )


@router.post(
    "/verify-reset-code",
    response_model=VerifyResetCodeResponse,
    dependencies=[Depends(reset_code_limiter)]
)
def verify_reset_code(
    data: VerifyResetCodeRequest,
    db: Session = Depends(get_db)
):
    """
    Comprueba el código sin usarlo. Los intentos
    fallidos cuentan para el límite del código.
    """

    return VerifyResetCodeResponse(
        valid=PasswordResetService.verify_code(
            db=db,
            email=data.email,
            code=data.code
        )
    )


@router.post(
    "/reset-password",
    response_model=MessageResponse,
    dependencies=[Depends(reset_code_limiter)]
)
def reset_password(
    data: ResetPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Cambia la contraseña con el código recibido y
    cierra todas las sesiones abiertas.
    """

    email = PasswordResetService.reset_password(
        db=db,
        email=data.email,
        code=data.code,
        new_password=data.new_password
    )

    background_tasks.add_task(email.send)

    return MessageResponse(
        message=RESET_PASSWORD_MESSAGE
    )
