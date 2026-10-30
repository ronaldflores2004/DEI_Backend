from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_patient_profile
)

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.audit.schemas.access_audit_response import (
    AccessAuditResponse
)

from app.audit.services.access_audit_service import (
    AccessAuditService
)


router = APIRouter(
    prefix="/audit",
    tags=["Audit"]
)


# =====================================
# Quién accedió a mis datos
# =====================================

@router.get(
    "/my-access-log",
    response_model=list[AccessAuditResponse]
)
def get_my_access_log(
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    return AccessAuditService.get_my_access_log(
        patient=patient,
        db=db
    )
