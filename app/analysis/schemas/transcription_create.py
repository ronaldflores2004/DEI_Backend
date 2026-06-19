from pydantic import BaseModel


class TranscriptionCreate(BaseModel):

    transcription_text: str