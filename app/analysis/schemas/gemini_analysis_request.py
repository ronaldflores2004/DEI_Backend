from pydantic import BaseModel


class GeminiAnalysisRequest(BaseModel):
    texto: str