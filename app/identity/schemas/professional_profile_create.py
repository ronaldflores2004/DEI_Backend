from pydantic import BaseModel, Field


class ProfessionalProfileCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    license_number: str = Field(min_length=1, max_length=100)
    specialties: str = Field(min_length=1, max_length=500)