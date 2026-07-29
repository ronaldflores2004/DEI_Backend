from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.identity.models.professional_profile import (
    ProfessionalProfile
)

from app.identity.repositories.professional_repository import (
    ProfessionalRepository
)

from app.shared.enums.link_request_status_enum import (
    LinkRequestStatusEnum
)

from app.shared.enums.sharing_mode_enum import (
    SharingModeEnum
)

from app.therapy.models.link_request import (
    LinkRequest
)

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


class LinkRequestService:
    """
    Servicio encargado de la gestión de
    solicitudes de vinculación.
    """

    @staticmethod
    def create_link_request(
        data: LinkRequestCreate,
        patient: PatientProfile,
        db: Session,
    ) -> LinkRequest:

        professional = (
            ProfessionalRepository.get_by_id(
                db=db,
                professional_id=data.professional_id
            )
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

        request = LinkRequest(
            patient_id=patient.id,
            professional_id=professional.id,
            status=LinkRequestStatusEnum.PENDING
        )

        return LinkRequestRepository.create(
            db=db,
            request=request
        )

    @staticmethod
    def get_pending_requests(
        professional: ProfessionalProfile,
        db: Session,
    ) -> list[LinkRequest]:

        return (
            LinkRequestRepository.get_pending_by_professional(
                db=db,
                professional_id=professional.id
            )
        )

    @staticmethod
    def accept_request(
        request_id: int,
        professional: ProfessionalProfile,
        db: Session,
    ) -> dict:

        request = LinkRequestRepository.get_by_id(
            db=db,
            request_id=request_id
        )

        if not request:
            raise HTTPException(
                status_code=404,
                detail="Solicitud no encontrada"
            )

        if request.professional_id != professional.id:
            raise HTTPException(
                status_code=403,
                detail="Solicitud no pertenece a este profesional"
            )

        if request.status != LinkRequestStatusEnum.PENDING:
            raise HTTPException(
                status_code=400,
                detail="La solicitud ya fue procesada"
            )

        existing_relation = (
            PatientProfessionalRepository.get_active_relation(
                db=db,
                patient_id=request.patient_id,
                professional_id=professional.id
            )
        )

        if existing_relation:
            raise HTTPException(
                status_code=400,
                detail="La relación terapéutica ya existe"
            )

        request.status = LinkRequestStatusEnum.ACCEPTED

        relation = PatientProfessional(
            patient_id=request.patient_id,
            professional_id=request.professional_id,
            sharing_mode=SharingModeEnum.FULL_HISTORY,
            active=True
        )

        try:

            LinkRequestRepository.update_no_commit(
                db=db,
                request=request
            )

            PatientProfessionalRepository.create_no_commit(
                db=db,
                relation=relation
            )

            db.commit()

            return {
                "message": "Solicitud aceptada"
            }

        except Exception:

            db.rollback()

            raise