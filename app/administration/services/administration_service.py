from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.identity.models.user import User

from app.identity.models.patient_profile import (
    PatientProfile
)

from app.identity.models.professional_profile import (
    ProfessionalProfile
)

from app.entries.repositories.emotional_entry_repository import (
    EmotionalEntryRepository
)

from app.analysis.repositories.emotional_analysis_repository import (
    EmotionalAnalysisRepository
)

from app.sessions.models.therapy_session import (
    TherapySession
)

from app.notifications.models.notification import (
    Notification
)

from app.recommendations.models.patient_recommendation import (
    PatientRecommendation
)


# ====================================================
# Dashboard general del sistema
# ====================================================

def get_admin_dashboard(
    db: Session
):

    return {

        "total_users":
            db.query(User).count(),

        "total_patients":
            db.query(PatientProfile).count(),

        "total_professionals":
            db.query(ProfessionalProfile).count(),

        "verified_professionals":
            db.query(ProfessionalProfile)
            .filter(
                ProfessionalProfile.is_verified == True
            )
            .count(),

        "pending_professionals":
            db.query(ProfessionalProfile)
            .filter(
                ProfessionalProfile.is_verified == False
            )
            .count(),

        "total_entries":
            EmotionalEntryRepository.count_all(
                db
            ),

        "total_analyses":
            EmotionalAnalysisRepository.count_all(
                db
            ),

        "total_sessions":
            db.query(TherapySession).count()
    }


# ====================================================
# Estadísticas generales
# ====================================================

def get_system_statistics(
    db: Session
):

    return {

        "active_users":
            db.query(User)
            .filter(
                User.is_active == True
            )
            .count(),

        "inactive_users":
            db.query(User)
            .filter(
                User.is_active == False
            )
            .count(),

        "archived_entries":
            EmotionalEntryRepository.count_archived(
                db
            ),

        "generated_recommendations":
            db.query(PatientRecommendation)
            .count(),

        "notifications_sent":
            db.query(Notification)
            .count()
    }


# ====================================================
# Usuarios
# ====================================================

def get_users(
    db: Session
):

    return (
        db.query(User)
        .order_by(
            User.email
        )
        .all()
    )


# ====================================================
# Activar usuario
# ====================================================

def activate_user(
    user_id: int,
    db: Session
):

    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
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

    db.commit()

    db.refresh(user)

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
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
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
            db.query(User)
            .filter(
                User.role == "ADMIN",
                User.is_active == True
            )
            .count()
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

    db.commit()

    db.refresh(user)

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
        db.query(ProfessionalProfile)
        .order_by(
            ProfessionalProfile.last_name,
            ProfessionalProfile.first_name
        )
        .all()
    )


# ====================================================
# Verificar profesional
# ====================================================

def verify_professional(
    professional_id: int,
    db: Session
):

    professional = (
        db.query(ProfessionalProfile)
        .filter(
            ProfessionalProfile.id == professional_id
        )
        .first()
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

    db.commit()

    db.refresh(professional)

    return {

        "id": professional.id,

        "first_name": professional.first_name,

        "last_name": professional.last_name,

        "is_verified": professional.is_verified,

        "message": "Profesional verificado"
    }