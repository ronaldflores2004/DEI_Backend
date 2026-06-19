from datetime import datetime

from pydantic import BaseModel


class TranscriptionResponse(BaseModel):

    id: int

    entry_id: int

    transcription_text: str

    provider: str

    created_at: datetime

    class Config:
        from_attributes = True