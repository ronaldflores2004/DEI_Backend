from pydantic import BaseModel

from app.shared.enums.insight_priority_enum import (
    InsightPriorityEnum
)


class TherapyInsightResponse(BaseModel):

    title: str

    content: str

    priority: InsightPriorityEnum
    