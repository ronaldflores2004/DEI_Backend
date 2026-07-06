from datetime import datetime

from sqlalchemy.orm import Session

from app.entries.models.emotional_entry import (
    EmotionalEntry,
)


class EmotionalEntryRepository:
    """
    Repositorio para el acceso a datos de
    EmotionalEntry.
    """

    # =====================================
    # CRUD
    # =====================================

    @staticmethod
    def get_by_id(
        db: Session,
        entry_id: int,
    ) -> EmotionalEntry | None:

        return (
            db.query(EmotionalEntry)
            .filter(
                EmotionalEntry.id == entry_id
            )
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        entry: EmotionalEntry,
    ) -> EmotionalEntry:

        db.add(entry)

        db.commit()

        db.refresh(entry)

        return entry

    @staticmethod
    def archive(
        db: Session,
        entry: EmotionalEntry,
    ) -> EmotionalEntry:

        entry.is_archived = True

        db.commit()

        db.refresh(entry)

        return entry

    # =====================================
    # CONSULTAS DE DOMINIO
    # =====================================

    @staticmethod
    def get_by_patient(
        db: Session,
        patient_id: int,
    ) -> list[EmotionalEntry]:

        return (
            db.query(EmotionalEntry)
            .filter(
                EmotionalEntry.patient_id == patient_id
            )
            .order_by(
                EmotionalEntry.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_latest_by_patient(
        db: Session,
        patient_id: int,
    ) -> EmotionalEntry | None:

        return (
            db.query(EmotionalEntry)
            .filter(
                EmotionalEntry.patient_id == patient_id
            )
            .order_by(
                EmotionalEntry.created_at.desc()
            )
            .first()
        )

    @staticmethod
    def count_by_patient(
        db: Session,
        patient_id: int,
    ) -> int:

        return (
            db.query(EmotionalEntry)
            .filter(
                EmotionalEntry.patient_id == patient_id
            )
            .count()
        )

    @staticmethod
    def get_text_entries(
        db: Session,
        patient_id: int,
    ) -> list[EmotionalEntry]:

        return (
            db.query(EmotionalEntry)
            .filter(
                EmotionalEntry.patient_id == patient_id,
                EmotionalEntry.entry_type == "TEXT"
            )
            .order_by(
                EmotionalEntry.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_audio_entries(
        db: Session,
        patient_id: int,
    ) -> list[EmotionalEntry]:

        return (
            db.query(EmotionalEntry)
            .filter(
                EmotionalEntry.patient_id == patient_id,
                EmotionalEntry.entry_type == "AUDIO"
            )
            .order_by(
                EmotionalEntry.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_recent_entries(
        db: Session,
        patient_id: int,
        since: datetime,
    ) -> list[EmotionalEntry]:

        return (
            db.query(EmotionalEntry)
            .filter(
                EmotionalEntry.patient_id == patient_id,
                EmotionalEntry.created_at >= since
            )
            .order_by(
                EmotionalEntry.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_archived_entries(
        db: Session,
        patient_id: int,
    ) -> list[EmotionalEntry]:

        return (
            db.query(EmotionalEntry)
            .filter(
                EmotionalEntry.patient_id == patient_id,
                EmotionalEntry.is_archived == True
            )
            .order_by(
                EmotionalEntry.created_at.desc()
            )
            .all()
        )
        
    @staticmethod
    def count_all(
        db: Session,
    ) -> int:

        return (
            db.query(EmotionalEntry)
            .count()
        )

    @staticmethod
    def count_archived(
        db: Session,
    ) -> int:

        return (
            db.query(EmotionalEntry)
            .filter(
                EmotionalEntry.is_archived == True
            )
            .count()
        )