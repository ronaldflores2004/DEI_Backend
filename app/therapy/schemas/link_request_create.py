from pydantic import BaseModel, Field


class LinkRequestCreate(BaseModel):
    professional_id: int = Field(gt=0)