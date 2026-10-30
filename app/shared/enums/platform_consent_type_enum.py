from enum import Enum


class PlatformConsentTypeEnum(str, Enum):
    # Consentimiento informado: qué es DEI, que no es
    # un servicio de emergencias y límites de la
    # confidencialidad.
    INFORMED_CONSENT = "INFORMED_CONSENT"
    # Procesamiento de las entradas con IA.
    AI_PROCESSING = "AI_PROCESSING"
