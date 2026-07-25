from datetime import date

from pydantic import BaseModel, Field

from app.shared.enums.gender_enum import GenderEnum


class PatientProfileCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    birth_date: date
    gender: GenderEnum