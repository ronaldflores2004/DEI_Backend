from pydantic import BaseModel


class ProfessionalProfileCreate(BaseModel):
    first_name: str
    last_name: str
    license_number: str
    specialties: str