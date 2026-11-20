from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import (
    get_current_professional_profile,
    get_current_user
)

from app.identity.models.professional_profile import (
    ProfessionalProfile
)

from app.identity.models.user import User

from app.identity.schemas.professional_profile_create import (
    ProfessionalProfileCreate
)

from app.identity.schemas.professional_profile_response import (
    ProfessionalProfileResponse
)

from app.identity.schemas.professional_portal import (
    ProfessionalDirectoryItem,
    ProfessionalPatientEntryResponse,
    ProfessionalPatientResponse,
)

from app.identity.services.professional_service import (
    ProfessionalService
)

from app.identity.services.professional_portal_service import (
    ProfessionalPortalService
)



router = APIRouter(
    prefix="/professionals",
    tags=["Professionals"]
)


@router.post(
    "/profile",
    response_model=ProfessionalProfileResponse
)
def create_professional_profile(
    profile: ProfessionalProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ProfessionalService.create_profile(
        db=db,
        current_user=current_user,
        profile=profile
    )


@router.get("/pending")
def get_pending_professionals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ProfessionalService.get_pending(
        db=db,
        current_user=current_user
    )


@router.patch("/{professional_id}/verify")
def verify_professional(
    professional_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ProfessionalService.verify_professional(
        professional_id=professional_id,
        db=db,
        current_user=current_user
    )


@router.get(
    "/profile/me",
    response_model=ProfessionalProfileResponse
)
def get_my_professional_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ProfessionalPortalService.get_my_profile(
        db=db,
        current_user=current_user
    )


@router.get(
    "/me/patients",
    response_model=list[ProfessionalPatientResponse]
)
def get_my_patients(
    db: Session = Depends(get_db),
    professional: ProfessionalProfile = Depends(
        get_current_professional_profile
    )
):

    return ProfessionalPortalService.get_my_patients(
        db=db,
        professional=professional
    )


@router.get(
    "/me/patients/{patient_id}/entries",
    response_model=list[ProfessionalPatientEntryResponse]
)
def get_patient_entries(
    patient_id: int,
    db: Session = Depends(get_db),
    professional: ProfessionalProfile = Depends(
        get_current_professional_profile
    )
):

    return ProfessionalPortalService.get_patient_entries(
        db=db,
        professional=professional,
        patient_id=patient_id
    )


@router.get(
    "/directory",
    response_model=list[ProfessionalDirectoryItem]
)
def get_professional_directory(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ProfessionalPortalService.get_directory(
        db=db
    )
