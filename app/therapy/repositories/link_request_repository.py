from sqlalchemy.orm import Session

from app.therapy.models.link_request import (
    LinkRequest,
)

from app.shared.enums.link_request_status_enum import (
    LinkRequestStatusEnum
)


class LinkRequestRepository:
    """
    Repositorio para el acceso a datos de
    LinkRequest.
    """

    @staticmethod
    def get_by_id(
        db: Session,
        request_id: int,
    ) -> LinkRequest | None:

        return (
            db.query(LinkRequest)
            .filter(
                LinkRequest.id == request_id
            )
            .first()
        )

    @staticmethod
    def get_pending_request(
        db: Session,
        patient_id: int,
        professional_id: int,
    ) -> LinkRequest | None:

        return (
            db.query(LinkRequest)
            .filter(
                LinkRequest.patient_id == patient_id,
                LinkRequest.professional_id == professional_id,
                LinkRequest.status == LinkRequestStatusEnum.PENDING,
            )
            .first()
        )

    @staticmethod
    def get_by_professional(
        db: Session,
        professional_id: int,
    ) -> list[LinkRequest]:

        return (
            db.query(LinkRequest)
            .filter(
                LinkRequest.professional_id == professional_id
            )
            .all()
        )

    @staticmethod
    def get_pending_by_professional(
        db: Session,
        professional_id: int,
    ) -> list[LinkRequest]:

        return (
            db.query(LinkRequest)
            .filter(
                LinkRequest.professional_id == professional_id,
                LinkRequest.status == LinkRequestStatusEnum.PENDING,
            )
            .all()
        )

    @staticmethod
    def create(
        db: Session,
        request: LinkRequest,
    ) -> LinkRequest:

        db.add(request)

        db.commit()

        db.refresh(request)

        return request
    
    @staticmethod
    def update(
        db: Session,
        request: LinkRequest,
    ) -> LinkRequest:

        db.commit()

        db.refresh(request)

        return request
    
    @staticmethod
    def update_no_commit(
        db: Session,
        request: LinkRequest,
    ) -> LinkRequest:

        db.flush()

        return request