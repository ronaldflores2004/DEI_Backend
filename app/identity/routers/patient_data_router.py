from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_patient_profile
)

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.identity.schemas.patient_data_erase import (
    PatientDataErase
)

from app.identity.services.patient_data_service import (
    PatientDataService
)


router = APIRouter(
    prefix="/patients/me/data",
    tags=["Patient Data"]
)


# =====================================
# Exportar mis datos
# =====================================

@router.get("/export")
def export_my_data(
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    return PatientDataService.export(
        patient=patient,
        db=db
    )


# =====================================
# Eliminar mis datos y desactivar la cuenta
# =====================================

@router.post("/erase")
def erase_my_data(
    data: PatientDataErase,
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    return PatientDataService.erase(
        patient=patient,
        confirmation=data.confirmation,
        db=db
    )
