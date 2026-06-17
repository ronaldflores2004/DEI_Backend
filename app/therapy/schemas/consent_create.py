from pydantic import BaseModel


class ConsentCreate(BaseModel):
    professional_id: int