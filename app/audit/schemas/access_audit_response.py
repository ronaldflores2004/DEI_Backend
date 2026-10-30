from datetime import datetime

from pydantic import BaseModel

from app.shared.enums.audit_action_enum import (
    AuditActionEnum
)


class AccessAuditResponse(BaseModel):

    professional_id: int

    professional_name: str

    action: AuditActionEnum

    created_at: datetime
