from datetime import datetime

from pydantic import BaseModel

from app.shared.enums.emotion_intensity_enum import (
    EmotionIntensityEnum
)

from app.shared.enums.risk_level_enum import (
    RiskLevelEnum
)

from app.analysis.schemas.crisis_support_response import (
    CrisisSupportResponse
)

class EmotionalAnalysisResponse(BaseModel):

    id: int

    entry_id: int

    primary_emotion: str | None

    emotion_intensity: EmotionIntensityEnum | None

    risk_level: RiskLevelEnum | None

    provider: str

    model: str

    analysis_json: dict

    analyzed_at: datetime

    # Solo se completa cuando el riesgo es HIGH
    # o CRITICAL, para mostrar ayuda inmediata.
    crisis_support: CrisisSupportResponse | None = None

    class Config:
        from_attributes = True