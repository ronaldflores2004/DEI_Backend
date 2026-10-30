import logging
import os
import secrets
from datetime import date, datetime

from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.identity.models.user import User

from app.entries.models.emotional_entry import (
    EmotionalEntry
)

from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis
)

from app.analysis.models.audio_transcription import (
    AudioTranscription
)

from app.recommendations.models.patient_recommendation import (
    PatientRecommendation
)

from app.risk_alerts.models.risk_alert import (
    RiskAlert
)

from app.notifications.models.notification import (
    Notification
)

from app.platform_consents.models.platform_consent import (
    PlatformConsent
)

from app.therapy.models.consent import Consent

from app.therapy.models.link_request import (
    LinkRequest
)

from app.therapy.models.patient_professional import (
    PatientProfessional
)

from app.sessions.models.therapy_session import (
    TherapySession
)

from app.shared.enums.link_request_status_enum import (
    LinkRequestStatusEnum
)

logger = logging.getLogger(__name__)

ERASE_CONFIRMATION = "ELIMINAR"


def _row(obj, fields: list[str]) -> dict:

    return {
        field: getattr(obj, field)
        for field in fields
    }


class PatientDataService:
    """
    Derechos del paciente sobre sus datos:
    exportarlos y eliminarlos.
    """

    @staticmethod
    def export(
        patient: PatientProfile,
        db: Session,
    ) -> dict:
        """
        Todos los datos del paciente en un JSON.
        Las notas clínicas no se incluyen: son el
        registro del profesional.
        """

        entries = (
            db.query(EmotionalEntry)
            .filter(EmotionalEntry.patient_id == patient.id)
            .order_by(EmotionalEntry.created_at)
            .all()
        )

        entry_ids = [entry.id for entry in entries]

        analyses = {
            analysis.entry_id: analysis
            for analysis in (
                db.query(EmotionalAnalysis)
                .filter(EmotionalAnalysis.entry_id.in_(entry_ids))
                .all()
            )
        }

        transcriptions = {
            transcription.entry_id: transcription
            for transcription in (
                db.query(AudioTranscription)
                .filter(AudioTranscription.entry_id.in_(entry_ids))
                .all()
            )
        }

        return {
            "exported_at": datetime.utcnow(),
            "profile": _row(
                patient,
                ["first_name", "last_name", "birth_date", "gender", "created_at"]
            ),
            "entries": [
                {
                    **_row(
                        entry,
                        ["id", "entry_type", "text_content", "is_archived", "created_at"]
                    ),
                    "transcription": (
                        transcriptions[entry.id].transcription_text
                        if entry.id in transcriptions
                        else None
                    ),
                    "analysis": (
                        _row(
                            analyses[entry.id],
                            [
                                "primary_emotion", "emotion_intensity",
                                "risk_level", "provider", "model",
                                "analysis_json", "analyzed_at",
                            ]
                        )
                        if entry.id in analyses
                        else None
                    ),
                }
                for entry in entries
            ],
            "recommendations": [
                _row(
                    recommendation,
                    ["title", "content", "source", "created_at"]
                )
                for recommendation in (
                    db.query(PatientRecommendation)
                    .filter(PatientRecommendation.patient_id == patient.id)
                    .all()
                )
            ],
            "professional_relations": [
                _row(
                    relation,
                    ["professional_id", "sharing_mode", "share_from", "active", "created_at", "ended_at"]
                )
                for relation in (
                    db.query(PatientProfessional)
                    .filter(PatientProfessional.patient_id == patient.id)
                    .all()
                )
            ],
            "professional_consents": [
                _row(
                    consent,
                    ["professional_id", "granted", "granted_at", "revoked_at"]
                )
                for consent in (
                    db.query(Consent)
                    .filter(Consent.patient_id == patient.id)
                    .all()
                )
            ],
            "platform_consents": [
                _row(
                    consent,
                    ["consent_type", "version", "granted_at", "revoked_at"]
                )
                for consent in (
                    db.query(PlatformConsent)
                    .filter(PlatformConsent.patient_id == patient.id)
                    .all()
                )
            ],
            "sessions": [
                _row(
                    session,
                    ["professional_id", "session_date", "status", "created_at"]
                )
                for session in (
                    db.query(TherapySession)
                    .filter(TherapySession.patient_id == patient.id)
                    .all()
                )
            ],
        }

    @staticmethod
    def erase(
        patient: PatientProfile,
        confirmation: str,
        db: Session,
    ) -> dict:
        """
        Elimina el diario (entradas, audios,
        transcripciones, análisis, recomendaciones y
        alertas), revoca consentimientos, cierra los
        vínculos y desactiva la cuenta.

        Se conservan, sin datos personales del
        paciente, las sesiones y notas clínicas
        (registro del profesional), el historial de
        consentimientos y la auditoría de accesos.
        """

        if confirmation != ERASE_CONFIRMATION:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Para eliminar tus datos escribe "
                    f"{ERASE_CONFIRMATION} en confirmation"
                )
            )

        now = datetime.utcnow()

        entries = (
            db.query(EmotionalEntry)
            .filter(EmotionalEntry.patient_id == patient.id)
            .all()
        )

        entry_ids = [entry.id for entry in entries]

        audio_paths = [
            entry.audio_path
            for entry in entries
            if entry.audio_path
        ]

        analysis_ids = [
            analysis_id
            for (analysis_id,) in (
                db.query(EmotionalAnalysis.id)
                .filter(EmotionalAnalysis.entry_id.in_(entry_ids))
                .all()
            )
        ]

        try:

            db.query(RiskAlert).filter(
                RiskAlert.patient_id == patient.id
            ).delete(synchronize_session=False)

            db.query(PatientRecommendation).filter(
                PatientRecommendation.patient_id == patient.id
            ).delete(synchronize_session=False)

            db.query(EmotionalAnalysis).filter(
                EmotionalAnalysis.id.in_(analysis_ids)
            ).delete(synchronize_session=False)

            db.query(AudioTranscription).filter(
                AudioTranscription.entry_id.in_(entry_ids)
            ).delete(synchronize_session=False)

            db.query(EmotionalEntry).filter(
                EmotionalEntry.id.in_(entry_ids)
            ).delete(synchronize_session=False)

            db.query(Notification).filter(
                Notification.user_id == patient.user_id
            ).delete(synchronize_session=False)

            db.query(LinkRequest).filter(
                LinkRequest.patient_id == patient.id,
                LinkRequest.status == LinkRequestStatusEnum.PENDING
            ).update(
                {"status": LinkRequestStatusEnum.REJECTED},
                synchronize_session=False
            )

            db.query(PatientProfessional).filter(
                PatientProfessional.patient_id == patient.id,
                PatientProfessional.active.is_(True)
            ).update(
                {"active": False, "ended_at": now},
                synchronize_session=False
            )

            db.query(Consent).filter(
                Consent.patient_id == patient.id,
                Consent.granted.is_(True)
            ).update(
                {"granted": False, "revoked_at": now},
                synchronize_session=False
            )

            db.query(PlatformConsent).filter(
                PlatformConsent.patient_id == patient.id,
                PlatformConsent.revoked_at.is_(None)
            ).update(
                {"revoked_at": now},
                synchronize_session=False
            )

            profile = db.get(PatientProfile, patient.id)
            profile.first_name = "Paciente"
            profile.last_name = "eliminado"
            # birth_date no admite nulos: fecha neutra.
            profile.birth_date = date(1900, 1, 1)

            user = db.get(User, patient.user_id)
            user.email = f"eliminado-{user.id}@dei.invalid"
            user.password_hash = secrets.token_hex(32)
            user.is_active = False

            db.commit()

        except Exception:

            db.rollback()
            raise

        for path in audio_paths:

            try:
                os.remove(path)

            except OSError:
                logger.warning(
                    "No se pudo borrar el audio %s",
                    path
                )

        return {
            "message": "Tus datos fueron eliminados y tu cuenta desactivada",
            "deleted_entries": len(entry_ids),
        }
