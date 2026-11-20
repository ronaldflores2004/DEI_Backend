from datetime import datetime

from pydantic import BaseModel


class ProfessionalPatientResponse(BaseModel):
    """
    Paciente con relación terapéutica activa,
    visto desde el panel del profesional.
    """

    patient_id: int

    first_name: str
    last_name: str

    sharing_mode: str
    share_from: datetime | None

    linked_at: datetime


class ProfessionalPatientEntryResponse(BaseModel):
    """
    Entrada del diario que el paciente comparte
    con el profesional, con su análisis si existe.
    """

    id: int

    entry_type: str
    text_content: str | None

    created_at: datetime

    primary_emotion: str | None = None
    emotion_intensity: str | None = None
    risk_level: str | None = None


class ProfessionalDirectoryItem(BaseModel):
    """
    Profesional verificado que un paciente
    puede elegir para vincularse.
    """

    id: int

    first_name: str
    last_name: str

    specialties: str

    class Config:
        from_attributes = True
