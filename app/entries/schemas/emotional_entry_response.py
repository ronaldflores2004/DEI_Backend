from datetime import datetime

from pydantic import BaseModel


class EmotionalEntryResponse(BaseModel):

    id: int

    patient_id: int

    entry_type: str

    text_content: str | None

    audio_path: str | None

    is_archived: bool

    created_at: datetime

    class Config:
        from_attributes = True