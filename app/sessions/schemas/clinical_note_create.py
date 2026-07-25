from pydantic import BaseModel, Field


class ClinicalNoteCreate(BaseModel):

    note: str = Field(min_length=1, max_length=20000)