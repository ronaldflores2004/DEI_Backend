from datetime import date, datetime

from pydantic import BaseModel


class PatientProfileResponse(BaseModel):

    id: int
    user_id: int

    first_name: str
    last_name: str

    birth_date: date

    gender: str

    created_at: datetime

    class Config:
        from_attributes = True