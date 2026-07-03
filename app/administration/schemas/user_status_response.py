from pydantic import BaseModel


class UserStatusResponse(BaseModel):

    id: int

    email: str

    is_active: bool

    message: str