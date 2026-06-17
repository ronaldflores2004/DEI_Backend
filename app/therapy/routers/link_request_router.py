from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.identity.models.user import User
from app.identity.models.patient_profile import PatientProfile
from app.identity.models.professional_profile import ProfessionalProfile

from app.therapy.models.link_request import LinkRequest

from app.therapy.schemas.link_request_create import (
    LinkRequestCreate
)

from app.therapy.schemas.link_request_response import (
    LinkRequestResponse
)

from app.therapy.models.patient_professional import (
    PatientProfessional
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
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "PATIENT":
        raise HTTPException(
            status_code=403,
            detail="Solo pacientes"
        )

    patient = (
        db.query(PatientProfile)
        .filter(
            PatientProfile.user_id == current_user.id
        )
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Perfil de paciente no encontrado"
        )

    professional = (
        db.query(ProfessionalProfile)
        .filter(
            ProfessionalProfile.id == request.professional_id
        )
        .first()
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
        db.query(LinkRequest)
        .filter(
            LinkRequest.patient_id == patient.id,
            LinkRequest.professional_id == professional.id,
            LinkRequest.status == "PENDING"
        )
        .first()
    )

    if existing_request:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una solicitud pendiente"
        )

    link_request = LinkRequest(
        patient_id=patient.id,
        professional_id=professional.id,
        status="PENDING"
    )

    db.add(link_request)

    db.commit()

    db.refresh(link_request)

    return link_request

@router.get("/pending")
def get_pending_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "PROFESSIONAL":
        raise HTTPException(
            status_code=403,
            detail="Solo profesionales"
        )

    professional = (
        db.query(ProfessionalProfile)
        .filter(
            ProfessionalProfile.user_id == current_user.id
        )
        .first()
    )

    if not professional:
        raise HTTPException(
            status_code=404,
            detail="Perfil profesional no encontrado"
        )

    requests = (
        db.query(LinkRequest)
        .filter(
            LinkRequest.professional_id == professional.id,
            LinkRequest.status == "PENDING"
        )
        .all()
    )

    return requests

@router.patch("/{request_id}/accept")
def accept_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "PROFESSIONAL":
        raise HTTPException(
            status_code=403,
            detail="Solo profesionales"
        )

    professional = (
        db.query(ProfessionalProfile)
        .filter(
            ProfessionalProfile.user_id == current_user.id
        )
        .first()
    )

    link_request = (
        db.query(LinkRequest)
        .filter(
            LinkRequest.id == request_id
        )
        .first()
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

    link_request.status = "ACCEPTED"

    relationship = PatientProfessional(
        patient_id=link_request.patient_id,
        professional_id=link_request.professional_id,
        sharing_mode="FULL_HISTORY",
        active=True
    )

    db.add(relationship)

    db.commit()

    return {
        "message": "Solicitud aceptada"
    }