from pydantic import BaseModel, Field


class PatientRecommendationCreate(BaseModel):

    title: str = Field(
        min_length=1,
        max_length=255
    )

    content: str = Field(
        min_length=1,
        max_length=10000
    )

    source: str = Field(
        min_length=1,
        max_length=50
    )