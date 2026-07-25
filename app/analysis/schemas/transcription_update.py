from pydantic import BaseModel, Field


class TranscriptionUpdate(BaseModel):

    transcription_text: str = Field(min_length=1, max_length=10000)