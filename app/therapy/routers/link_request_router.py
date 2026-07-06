from fastapi import APIRouter, Depends, HTTPException
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

from app.identity.repositories.professional_repository import (
    ProfessionalRepository
)

from app.therapy.models.link_request import LinkRequest

from app.therapy.models.patient_professional import (
    PatientProfessional
)

from app.therapy.repositories.link_request_repository import (
    LinkRequestRepository
)

from app.therapy.repositories.patient_professional_repository import (
    PatientProfessionalRepository
)

from app.therapy.schemas.link_request_create import (
    LinkRequestCreate
)

from app.therapy.schemas.link_request_response import (
    LinkRequestResponse
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

    professional = ProfessionalRepository.get_by_id(
        db,
        request.professional_id
    )

    if not professional:
        raise HTTPException(
            status_code=404,
            detail="Profesional no encontrado"
        )

    if not professional.is_verified:
        raise HTTPException(
            status_code=400,
            detail="Profesional no verificado"
        )

    existing_request = (
        LinkRequestRepository.get_pending_request(
            db=db,
            patient_id=patient.id,
            professional_id=professional.id
        )
    )

    if existing_request:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una solicitud pendiente"
        )

    existing_relation = (
        PatientProfessionalRepository.get_active_relation(
            db=db,
            patient_id=patient.id,
            professional_id=professional.id
        )
    )

    if existing_relation:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una relación terapéutica activa"
        )

    link_request = LinkRequest(
        patient_id=patient.id,
        professional_id=professional.id,
        status="PENDING"
    )

    link_request = LinkRequestRepository.create(
        db,
        link_request
    )

    return link_request


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

    return (
        LinkRequestRepository.get_pending_by_professional(
            db,
            professional.id
        )
    )


@router.patch("/{request_id}/accept")
def accept_request(
    request_id: int,
    db: Session = Depends(get_db),
    professional: ProfessionalProfile = Depends(
        get_current_professional_profile
    )
):

    link_request = LinkRequestRepository.get_by_id(
        db,
        request_id
    )

    if not link_request:
        raise HTTPException(
            status_code=404,
            detail="Solicitud no encontrada"
        )

    if link_request.professional_id != professional.id:
        raise HTTPException(
            status_code=403,
            detail="Solicitud no pertenece a este profesional"
        )

    existing_relation = (
        PatientProfessionalRepository.get_active_relation(
            db=db,
            patient_id=link_request.patient_id,
            professional_id=professional.id
        )
    )

    if existing_relation:
        raise HTTPException(
            status_code=400,
            detail="La relación terapéutica ya existe"
        )

    if link_request.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="La solicitud ya fue procesada"
        )

    link_request.status = "ACCEPTED"

    relationship = PatientProfessional(
        patient_id=link_request.patient_id,
        professional_id=link_request.professional_id,
        sharing_mode="FULL_HISTORY",
        active=True
    )

    PatientProfessionalRepository.create(
        db,
        relationship
    )

    return {
        "message": "Solicitud aceptada"
    }