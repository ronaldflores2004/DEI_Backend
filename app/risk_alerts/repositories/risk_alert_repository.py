from sqlalchemy.orm import Session

from app.risk_alerts.models.risk_alert import (
    RiskAlert
)


class RiskAlertRepository:
    """
    Repositorio para el acceso a datos de
    RiskAlert.
    """

    @staticmethod
    def get_by_id(
        db: Session,
        alert_id: int,
    ) -> RiskAlert | None:

        return (
            db.query(RiskAlert)
            .filter(
                RiskAlert.id == alert_id
            )
            .first()
        )

    @staticmethod
    def get_by_analysis_and_professional(
        db: Session,
        analysis_id: int,
        professional_id: int,
    ) -> RiskAlert | None:

        return (
            db.query(RiskAlert)
            .filter(
                RiskAlert.analysis_id == analysis_id,
                RiskAlert.professional_id == professional_id,
            )
            .first()
        )

    @staticmethod
    def get_by_professional(
        db: Session,
        professional_id: int,
        status: str | None = None,
    ) -> list[RiskAlert]:

        query = (
            db.query(RiskAlert)
            .filter(
                RiskAlert.professional_id == professional_id
            )
        )

        if status:
            query = query.filter(
                RiskAlert.status == status
            )

        return (
            query
            .order_by(
                RiskAlert.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def create_no_commit(
        db: Session,
        alert: RiskAlert,
    ) -> RiskAlert:

        db.add(alert)
        db.flush()

        return alert

    @staticmethod
    def update(
        db: Session,
        alert: RiskAlert,
    ) -> RiskAlert:

        db.commit()
        db.refresh(alert)

        return alert
