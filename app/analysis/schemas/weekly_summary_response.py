from pydantic import BaseModel


class WeeklySummaryResponse(BaseModel):

    entries_count: int

    dominant_emotion: str | None

    latest_emotion: str | None
    
    average_intensity: str | None

    risk_level: str | None

    trend: str

    recommendation: str