from pydantic import BaseModel


class EmotionalAnalysisCreate(BaseModel):

    primary_emotion: str

    emotion_intensity: str

    risk_level: str

    analysis_json: dict