from pydantic import BaseModel


class TherapyInsightResponse(BaseModel):

    title: str

    content: str

    priority: str