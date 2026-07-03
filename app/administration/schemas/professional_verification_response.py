from pydantic import BaseModel


class ProfessionalVerificationResponse(BaseModel):

    id: int

    first_name: str

    last_name: str

    is_verified: bool

    message: str