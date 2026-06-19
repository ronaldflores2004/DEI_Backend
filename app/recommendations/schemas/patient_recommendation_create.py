from pydantic import BaseModel


class PatientRecommendationCreate(BaseModel):

    title: str

    content: str

    source: str