from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.administration.models.crisis_line import (
    CrisisLine
)

from app.administration.repositories.crisis_line_repository import (
    CrisisLineRepository
)

from app.administration.repositories.system_setting_repository import (
    SystemSettingRepository
)

from app.administration.schemas.crisis_line_schemas import (
    CrisisLineCreate,
    CrisisLineUpdate
)

from app.core.config import settings

from app.identity.models.user import User

from app.shared.ai.runtime_settings import (
    AI_PROVIDER_CHAIN_KEY,
    SUPPORTED_PROVIDERS,
    clear_cache,
    parse_chain,
    validate_chain
)


class AdminSettingsService:
    """
    Ajustes que el administrador gestiona desde
    el panel: líneas de crisis y proveedor de IA.
    """

    # =====================================
    # Líneas de crisis
    # =====================================

    @staticmethod
    def list_crisis_lines(
        db: Session,
        country_code: str | None = None,
    ) -> list[CrisisLine]:

        return CrisisLineRepository.get_all(
            db=db,
            country_code=country_code
        )

    @staticmethod
    def create_crisis_line(
        data: CrisisLineCreate,
        db: Session,
    ) -> CrisisLine:

        return CrisisLineRepository.save(
            db=db,
            line=CrisisLine(
                country_code=data.country_code.upper(),
                city=data.city,
                name=data.name,
                phone=data.phone,
                sort_order=data.sort_order,
                is_active=data.is_active,
            )
        )

    @staticmethod
    def update_crisis_line(
        line_id: int,
        data: CrisisLineUpdate,
        db: Session,
    ) -> CrisisLine:

        line = CrisisLineRepository.get_by_id(
            db=db,
            line_id=line_id
        )

        if not line:
            raise HTTPException(
                status_code=404,
                detail="Línea de crisis no encontrada"
            )

        for field, value in data.model_dump(
            exclude_unset=True
        ).items():
            setattr(line, field, value)

        return CrisisLineRepository.save(
            db=db,
            line=line
        )

    # =====================================
    # Proveedor de IA
    # =====================================

    @staticmethod
    def get_ai_settings(
        db: Session,
    ) -> dict:

        setting = SystemSettingRepository.get(
            db=db,
            key=AI_PROVIDER_CHAIN_KEY
        )

        return {
            "provider_chain": (
                parse_chain(setting.value)
                if setting
                else settings.AI_PROVIDER_CHAIN
            ),
            "source": "admin" if setting else "env",
            "supported_providers": SUPPORTED_PROVIDERS,
        }

    @staticmethod
    def update_ai_settings(
        provider_chain: list[str],
        current_user: User,
        db: Session,
    ) -> dict:

        chain = parse_chain(provider_chain)

        try:
            validate_chain(chain)

        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            ) from e

        SystemSettingRepository.set(
            db=db,
            key=AI_PROVIDER_CHAIN_KEY,
            value=",".join(chain),
            user_id=current_user.id
        )

        clear_cache()

        return AdminSettingsService.get_ai_settings(db)

    @staticmethod
    def reset_ai_settings(
        db: Session,
    ) -> dict:

        SystemSettingRepository.delete(
            db=db,
            key=AI_PROVIDER_CHAIN_KEY
        )

        clear_cache()

        return AdminSettingsService.get_ai_settings(db)
