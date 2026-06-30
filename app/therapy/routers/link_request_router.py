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
    patient: PatientProfile = Depends(
        get_current_patient_profile
    )
):

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
    
    existing_relation = (
        db.query(PatientProfessional)
        .filter(
            PatientProfessional.patient_id == patient.id,
            PatientProfessional.professional_id == professional.id,
            PatientProfessional.active == True
        )
        .first()
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

    db.add(link_request)

    db.commit()

    db.refresh(link_request)

    return link_request

@router.get("/pending")
def get_pending_requests(
    db: Session = Depends(get_db),
    professional: ProfessionalProfile = Depends(
        get_current_professional_profile
    )
):

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
    professional: ProfessionalProfile = Depends(
        get_current_professional_profile
    )
):

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
    
    existing_relation = (
        db.query(PatientProfessional)
        .filter(
            PatientProfessional.patient_id
            == link_request.patient_id,
            PatientProfessional.professional_id
            == professional.id,
            PatientProfessional.active == True
        )
        .first()
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

    db.add(relationship)

    db.commit()

    return {
        "message": "Solicitud aceptada"
    }