from datetime import datetime

from pydantic import BaseModel


class ClinicalNoteResponse(BaseModel):

    id: int

    session_id: int

    professional_id: int

    note: str

    created_at: datetime

    class Config:
        from_attributes = True