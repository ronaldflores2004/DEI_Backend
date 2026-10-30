from enum import Enum


class RecommendationStatusEnum(str, Enum):
    # Generada por IA, espera revisión del profesional.
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
