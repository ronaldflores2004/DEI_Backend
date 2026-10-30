from pydantic import BaseModel, Field


class RecommendationApprove(BaseModel):
    """
    El profesional puede ajustar el texto
    antes de aprobarlo.
    """

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    content: str | None = Field(
        default=None,
        min_length=1,
        max_length=10000
    )
