from pydantic import BaseModel, Field


class AISettingsUpdate(BaseModel):

    # Orden en que se prueban, por ejemplo
    # ["OLLAMA", "GEMINI"].
    provider_chain: list[str] = Field(
        min_length=1
    )


class AISettingsResponse(BaseModel):

    provider_chain: list[str]

    # "admin" si lo eligió el administrador,
    # "env" si viene del .env.
    source: str

    supported_providers: list[str]
