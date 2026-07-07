from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.repositories.user_repository import (
    UserRepository
)

from app.identity.repositories.patient_repository import (
    PatientRepository
)

from app.identity.repositories.professional_repository import (
    ProfessionalRepository
)

from app.entries.repositories.emotional_entry_repository import (
    EmotionalEntryRepository
)

from app.analysis.repositories.emotional_analysis_repository import (
    EmotionalAnalysisRepository
)

from app.sessions.repositories.therapy_session_repository import (
    TherapySessionRepository
)

from app.notifications.repositories.notification_repository import (
    NotificationRepository
)

from app.recommendations.repositories.patient_recommendation_repository import (
    PatientRecommendationRepository
)


# ====================================================
# Dashboard general del sistema
# ====================================================

def get_admin_dashboard(
    db: Session
):

    return {

        "total_users":
            UserRepository.count_all(
                db
            ),

        "total_patients":
            PatientRepository.count_all(
                db
            ),

        "total_professionals":
            ProfessionalRepository.count_all(
                db
            ),

        "verified_professionals":
            ProfessionalRepository.count_verified(
                db
            ),

        "pending_professionals":
            ProfessionalRepository.count_pending(
                db
            ),

        "total_entries":
            EmotionalEntryRepository.count_all(
                db
            ),

        "total_analyses":
            EmotionalAnalysisRepository.count_all(
                db
            ),

        "total_sessions":
            TherapySessionRepository.count_all(
                db
            )
    }


# ====================================================
# Estadísticas generales
# ====================================================

def get_system_statistics(
    db: Session
):

    return {

        "active_users":
            UserRepository.count_active(
                db
            ),

        "inactive_users":
            UserRepository.count_inactive(
                db
            ),

        "archived_entries":
            EmotionalEntryRepository.count_archived(
                db
            ),

        "generated_recommendations":
            PatientRecommendationRepository.count_all(
                db
            ),

        "notifications_sent":
            NotificationRepository.count_all(
                db
            )
    }


# ====================================================
# Usuarios
# ====================================================

def get_users(
    db: Session
):

    return (
        UserRepository.get_all(
            db
        )
    )


# ====================================================
# Activar usuario
# ====================================================

def activate_user(
    user_id: int,
    db: Session
):

    user = (
        UserRepository.get_by_id(
            db,
            user_id
        )
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if user.is_active:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya está activo"
        )

    user.is_active = True

    UserRepository.update(
        db,
        user
    )

    return {

        "id": user.id,

        "email": user.email,

        "is_active": user.is_active,

        "message": "Usuario activado"
    }


# ====================================================
# Desactivar usuario
# ====================================================

def deactivate_user(
    user_id: int,
    current_admin_id: int,
    db: Session
):

    user = (
        UserRepository.get_by_id(
            db,
            user_id
        )
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if user.id == current_admin_id:
        raise HTTPException(
            status_code=400,
            detail="No puedes desactivar tu propia cuenta"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya está desactivado"
        )

    if user.role == "ADMIN":

        active_admins = (
            UserRepository.count_active_admins(
                db
            )
        )

        if active_admins <= 1:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Debe existir al menos un "
                    "administrador activo"
                )
            )

    user.is_active = False

    UserRepository.update(
        db,
        user
    )

    return {

        "id": user.id,

        "email": user.email,

        "is_active": user.is_active,

        "message": "Usuario desactivado"
    }


# ====================================================
# Profesionales
# ====================================================

def get_professionals(
    db: Session
):

    return (
        ProfessionalRepository.get_all(
            db
        )
    )


# ====================================================
# Verificar profesional
# ====================================================

def verify_professional(
    professional_id: int,
    db: Session
):

    professional = (
        ProfessionalRepository.get_by_id(
            db,
            professional_id
        )
    )

    if not professional:
        raise HTTPException(
            status_code=404,
            detail="Profesional no encontrado"
        )

    if professional.is_verified:
        raise HTTPException(
            status_code=400,
            detail="El profesional ya está verificado"
        )

    professional.is_verified = True

    ProfessionalRepository.update(
        db,
        professional
    )

    return {

        "id": professional.id,

        "first_name": professional.first_name,

        "last_name": professional.last_name,

        "is_verified": professional.is_verified,

        "message": "Profesional verificado"
    }