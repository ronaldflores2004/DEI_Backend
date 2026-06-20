from pydantic import BaseModel


class RiskAlertResponse(BaseModel):

    patient_id: int

    highest_risk: str

    alerts_count: int

    latest_emotion: str

    negative_emotions_count: int

    message: str