from datetime import datetime

from pydantic import BaseModel, Field


class CrisisLineCreate(BaseModel):

    country_code: str = Field(
        min_length=2,
        max_length=2
    )

    city: str | None = Field(
        default=None,
        max_length=100
    )

    name: str = Field(
        min_length=1,
        max_length=255
    )

    phone: str = Field(
        min_length=1,
        max_length=50
    )

    sort_order: int = 0

    is_active: bool = True


class CrisisLineUpdate(BaseModel):

    city: str | None = Field(
        default=None,
        max_length=100
    )

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    phone: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    sort_order: int | None = None

    is_active: bool | None = None


class CrisisLineResponse(BaseModel):

    id: int

    country_code: str

    city: str | None

    name: str

    phone: str

    sort_order: int

    is_active: bool

    updated_at: datetime

    class Config:
        from_attributes = True
