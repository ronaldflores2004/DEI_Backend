from sqlalchemy.orm import Session

from app.sessions.models.therapy_session import (
    TherapySession,
)


class TherapySessionRepository:
    """
    Repositorio para el acceso a datos de
    TherapySession.
    """

    @staticmethod
    def get_by_id(
        db: Session,
        session_id: int,
    ) -> TherapySession | None:

        return (
            db.query(TherapySession)
            .filter(
                TherapySession.id == session_id
            )
            .first()
        )

    @staticmethod
    def get_by_patient(
        db: Session,
        patient_id: int,
    ) -> list[TherapySession]:

        return (
            db.query(TherapySession)
            .filter(
                TherapySession.patient_id == patient_id
            )
            .order_by(
                TherapySession.session_date.desc()
            )
            .all()
        )

    @staticmethod
    def get_by_professional(
        db: Session,
        professional_id: int,
    ) -> list[TherapySession]:

        return (
            db.query(TherapySession)
            .filter(
                TherapySession.professional_id
                == professional_id
            )
            .order_by(
                TherapySession.session_date.desc()
            )
            .all()
        )

    @staticmethod
    def create(
        db: Session,
        session: TherapySession,
    ) -> TherapySession:

        db.add(session)

        db.commit()

        db.refresh(session)

        return session
    
    @staticmethod
    def create_no_commit(
        db: Session,
        session: TherapySession,
    ) -> TherapySession:

        db.add(session)
        db.flush()

        return session

    @staticmethod
    def update(
        db: Session,
        session: TherapySession,
    ) -> TherapySession:

        db.commit()

        db.refresh(session)

        return session

    @staticmethod
    def count_all(
        db: Session,
    ) -> int:

        return (
            db.query(TherapySession)
            .count()
        )