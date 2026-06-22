from pydantic import BaseModel


class ClinicalNoteCreate(BaseModel):

    note: str