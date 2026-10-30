from datetime import datetime

from pydantic import BaseModel, Field

from app.shared.enums.risk_alert_status_enum import (
    RiskAlertStatusEnum
)

from app.shared.enums.risk_level_enum import (
    RiskLevelEnum
)


class RiskAlertItemResponse(BaseModel):

    id: int

    patient_id: int

    analysis_id: int

    risk_level: RiskLevelEnum

    status: RiskAlertStatusEnum

    created_at: datetime

    seen_at: datetime | None

    resolved_at: datetime | None

    resolution_note: str | None

    class Config:
        from_attributes = True


class RiskAlertResolve(BaseModel):

    resolution_note: str = Field(
        min_length=1,
        max_length=1000
    )
