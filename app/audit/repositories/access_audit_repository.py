from sqlalchemy.orm import Session

from app.audit.models.access_audit_log import (
    AccessAuditLog
)


class AccessAuditRepository:
    """
    Repositorio para el acceso a datos de
    AccessAuditLog.
    """

    @staticmethod
    def create_many(
        db: Session,
        logs: list[AccessAuditLog],
    ) -> None:

        db.add_all(logs)
        db.commit()

    @staticmethod
    def get_by_patient(
        db: Session,
        patient_id: int,
        limit: int = 200,
    ) -> list[AccessAuditLog]:

        return (
            db.query(AccessAuditLog)
            .filter(
                AccessAuditLog.patient_id == patient_id
            )
            .order_by(
                AccessAuditLog.created_at.desc()
            )
            .limit(limit)
            .all()
        )
