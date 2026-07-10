from pydantic import BaseModel


class TranscriptionUpdate(BaseModel):

    transcription_text: str