from pydantic import BaseModel


class WeeklySummaryResponse(BaseModel):

    entries_count: int

    dominant_emotion: str | None

    risk_level: str | None

    recommendation: str