from datetime import datetime

from pydantic import BaseModel


class ProfessionalProfileResponse(BaseModel):

    id: int
    user_id: int

    first_name: str
    last_name: str

    license_number: str
    specialties: str

    is_verified: bool

    created_at: datetime

    class Config:
        from_attributes = True