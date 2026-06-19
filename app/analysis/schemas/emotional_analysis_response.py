from datetime import datetime

from pydantic import BaseModel


class EmotionalAnalysisResponse(BaseModel):

    id: int

    entry_id: int

    primary_emotion: str | None

    emotion_intensity: str | None

    risk_level: str | None

    analysis_json: dict

    analyzed_at: datetime

    class Config:
        from_attributes = True