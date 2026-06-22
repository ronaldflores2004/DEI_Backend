from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.entries.models.emotional_entry import (
    EmotionalEntry
)

from app.analysis.models.emotional_analysis import (
    EmotionalAnalysis
)

from app.analysis.services.fake_analysis_service import (
    analyze_text
)

from app.shared.enums.entry_type_enum import (
    EntryTypeEnum
)

from app.analysis.models.audio_transcription import (
    AudioTranscription
)

from app.analysis.services.gemini_analysis_service import (
    analyze_text_with_gemini
)

def create_analysis(
    entry_id: int,
    current_user_id: int,
    data,
    db: Session
):

    entry = (
        db.query(EmotionalEntry)
        .filter(
            EmotionalEntry.id == entry_id
        )
        .first()
    )

    if not entry:
        raise HTTPException(
            status_code=404,
            detail="Entrada no encontrada"
        )

    patient = (
        db.query(PatientProfile)
        .filter(
            PatientProfile.user_id == current_user_id
        )
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=403,
            detail="No tienes perfil de paciente"
        )

    if entry.patient_id != patient.id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para analizar esta entrada"
        )

    existing = (
        db.query(EmotionalAnalysis)
        .filter(
            EmotionalAnalysis.entry_id == entry_id
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="La entrada ya tiene análisis"
        )

    analysis = EmotionalAnalysis(
        entry_id=entry.id,
        primary_emotion=data.primary_emotion,
        emotion_intensity=data.emotion_intensity,
        risk_level=data.risk_level,
        analysis_json=data.analysis_json
    )

    db.add(analysis)

    db.commit()

    db.refresh(analysis)

    return analysis


def get_analysis(
    entry_id: int,
    current_user_id: int,
    db: Session
):

    analysis = (
        db.query(EmotionalAnalysis)
        .filter(
            EmotionalAnalysis.entry_id == entry_id
        )
        .first()
    )

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Análisis no encontrado"
        )

    entry = (
        db.query(EmotionalEntry)
        .filter(
            EmotionalEntry.id == entry_id
        )
        .first()
    )

    if not entry:
        raise HTTPException(
            status_code=404,
            detail="Entrada no encontrada"
        )

    patient = (
        db.query(PatientProfile)
        .filter(
            PatientProfile.user_id == current_user_id
        )
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=403,
            detail="No tienes perfil de paciente"
        )

    if entry.patient_id != patient.id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para ver este análisis"
        )

    return analysis

def create_analysis_from_entry(
    entry_id: int,
    current_user_id: int,
    db: Session
):

    entry = (
        db.query(EmotionalEntry)
        .filter(
            EmotionalEntry.id == entry_id
        )
        .first()
    )

    if not entry:
        raise HTTPException(
            status_code=404,
            detail="Entrada no encontrada"
        )

    text_to_analyze = None

    if entry.entry_type == EntryTypeEnum.TEXT:

        text_to_analyze = entry.text_content

    elif entry.entry_type == EntryTypeEnum.AUDIO:

        transcription = (
            db.query(AudioTranscription)
            .filter(
                AudioTranscription.entry_id == entry.id
            )
            .first()
        )

        if not transcription:
            raise HTTPException(
                status_code=400,
                detail="El audio aún no tiene transcripción"
            )

        text_to_analyze = (
            transcription.transcription_text
        )

    else:
        raise HTTPException(
            status_code=400,
            detail="Tipo de entrada no soportado"
        )

    if not text_to_analyze:
        raise HTTPException(
            status_code=400,
            detail="No existe texto para analizar"
        )

    patient = (
        db.query(PatientProfile)
        .filter(
            PatientProfile.user_id == current_user_id
        )
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=403,
            detail="No tienes perfil de paciente"
        )

    if entry.patient_id != patient.id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso"
        )

    existing = (
        db.query(EmotionalAnalysis)
        .filter(
            EmotionalAnalysis.entry_id == entry_id
        )
        .first()
    )

    if existing:
        return existing

    try:

        result = (
            analyze_text_with_gemini(
                text_to_analyze
            )
        )

    except Exception as e:

        print("ERROR GEMINI:")
        print(e)

        result = analyze_text(
            text_to_analyze
        )

    analysis = EmotionalAnalysis(
        entry_id=entry.id,
        primary_emotion=result["primary_emotion"],
        emotion_intensity=result["emotion_intensity"],
        risk_level=result["risk_level"],
        analysis_json=result["analysis_json"]
    )

    db.add(analysis)

    db.commit()

    db.refresh(analysis)

    return analysis