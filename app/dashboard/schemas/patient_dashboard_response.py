from pydantic import BaseModel


class PatientDashboardResponse(BaseModel):

    entries_count: int

    dominant_emotion: str | None

    latest_emotion: str | None

    average_intensity: str | None

    trend: str

    latest_recommendation: str | None