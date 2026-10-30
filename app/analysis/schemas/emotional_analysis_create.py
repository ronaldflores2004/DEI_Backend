from pydantic import BaseModel, Field

from app.shared.enums.emotion_intensity_enum import (
    EmotionIntensityEnum
)

class EmotionalAnalysisCreate(BaseModel):
    """
    Análisis manual del paciente.

    No incluye risk_level: el nivel de riesgo
    lo determina el sistema, nunca el paciente.
    """

    primary_emotion: str = Field(
        min_length=1,
        max_length=100
    )

    emotion_intensity: EmotionIntensityEnum

    analysis_json: dict