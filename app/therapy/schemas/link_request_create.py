from pydantic import BaseModel


class LinkRequestCreate(BaseModel):
    professional_id: int