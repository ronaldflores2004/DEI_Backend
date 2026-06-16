from datetime import date

from pydantic import BaseModel

from app.shared.enums.gender_enum import GenderEnum


class PatientProfileCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    gender: GenderEnum