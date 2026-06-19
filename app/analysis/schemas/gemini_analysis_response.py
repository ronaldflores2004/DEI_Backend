from pydantic import BaseModel


class GeminiAnalysisResponse(BaseModel):
    success: bool
    analisis: dict | None = None
    error: str | None = None