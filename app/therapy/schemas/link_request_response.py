from datetime import datetime

from pydantic import BaseModel


class LinkRequestResponse(BaseModel):

    id: int

    patient_id: int
    professional_id: int

    # Nombre del paciente para que el profesional
    # sepa quién envía la solicitud.
    patient_first_name: str | None = None
    patient_last_name: str | None = None

    status: str

    sharing_mode: str

    share_from: datetime | None

    created_at: datetime

    class Config:
        from_attributes = True