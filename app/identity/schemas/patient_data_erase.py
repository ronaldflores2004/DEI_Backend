from pydantic import BaseModel


class PatientDataErase(BaseModel):

    # Debe ser "ELIMINAR" para confirmar.
    confirmation: str
