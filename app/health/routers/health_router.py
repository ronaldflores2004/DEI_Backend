from fastapi import (
    APIRouter,
    Depends
)

from app.core.config import (
    settings
)

from app.core.dependencies import (
    require_role
)

from app.identity.models.user import User

from app.shared.ai.ollama_client import (
    OllamaClient
)

from app.shared.enums.role_enum import (
    RoleEnum
)

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


# =====================================
# Estado de los proveedores de IA
# =====================================

@router.get("/ai")
def ai_health(
    current_user: User = Depends(
        require_role(RoleEnum.ADMIN)
    )
):

    return {
        "provider_chain": settings.AI_PROVIDER_CHAIN,
        "ollama": OllamaClient.health(),
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "transcription_provider": settings.TRANSCRIPTION_PROVIDER
    }
