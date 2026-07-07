from sqlalchemy.orm import Session

from app.sessions.models.clinical_note import (
    ClinicalNote,
)


class ClinicalNoteRepository:
    """
    Repositorio para el acceso a datos de
    ClinicalNote.
    """

    @staticmethod
    def get_by_id(
        db: Session,
        note_id: int,
    ) -> ClinicalNote | None:

        return (
            db.query(ClinicalNote)
            .filter(
                ClinicalNote.id == note_id
            )
            .first()
        )

    @staticmethod
    def get_by_session(
        db: Session,
        session_id: int,
    ) -> list[ClinicalNote]:

        return (
            db.query(ClinicalNote)
            .filter(
                ClinicalNote.session_id
                == session_id
            )
            .order_by(
                ClinicalNote.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_by_professional(
        db: Session,
        professional_id: int,
    ) -> list[ClinicalNote]:

        return (
            db.query(ClinicalNote)
            .filter(
                ClinicalNote.professional_id
                == professional_id
            )
            .order_by(
                ClinicalNote.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def create(
        db: Session,
        note: ClinicalNote,
    ) -> ClinicalNote:

        db.add(note)

        db.commit()

        db.refresh(note)

        return note

    @staticmethod
    def update(
        db: Session,
        note: ClinicalNote,
    ) -> ClinicalNote:

        db.commit()

        db.refresh(note)

        return note

    @staticmethod
    def count_all(
        db: Session,
    ) -> int:

        return (
            db.query(ClinicalNote)
            .count()
        )