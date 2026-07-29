from pydantic import BaseModel, Field


class ConsentCreate(BaseModel):
    professional_id: int = Field(gt=0)