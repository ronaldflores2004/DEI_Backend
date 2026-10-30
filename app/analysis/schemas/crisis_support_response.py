from pydantic import BaseModel


class CrisisLineResponse(BaseModel):

    name: str

    phone: str


class CrisisSupportResponse(BaseModel):

    message: str

    lines: list[CrisisLineResponse]

    professional_notified: bool
