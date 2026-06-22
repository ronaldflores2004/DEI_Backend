from pydantic import BaseModel


class SessionStatusResponse(BaseModel):

    id: int

    status: str

    class Config:
        from_attributes = True