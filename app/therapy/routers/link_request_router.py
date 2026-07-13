from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_patient_profile,
    get_current_professional_profile
)

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.identity.models.professional_profile import (
    ProfessionalProfile
)

from app.therapy.schemas.link_request_create import (
    LinkRequestCreate
)

from app.therapy.schemas.link_request_response import (
    LinkRequestResponse
)

from app.therapy.services.link_request_service import (
    LinkRequestService
)

router = APIRouter(
    prefix="/therapy/link-requests",
    tags=["Link Requests"]
)


@router.post(
    "",
    response_model=LinkRequestResponse
)
def create_link_request(
    request: LinkRequestCreate,
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

    return LinkRequestService.create_link_request(
        data=request,
        patient=patient,
        db=db
    )


@router.get(
    "/pending",
    response_model=list[LinkRequestResponse]
)
def get_pending_requests(
    db: Session = Depends(get_db),
    professional: ProfessionalProfile = Depends(
        get_current_professional_profile
    )
):

    return LinkRequestService.get_pending_requests(
        professional=professional,
        db=db
    )


@router.patch("/{request_id}/accept")
def accept_request(
    request_id: int,
    db: Session = Depends(get_db),
    professional: ProfessionalProfile = Depends(
        get_current_professional_profile
    )
):

    return LinkRequestService.accept_request(
        request_id=request_id,
        professional=professional,
        db=db
    )