from app.shared.enums.platform_consent_type_enum import (
    PlatformConsentTypeEnum
)


# =====================================
# TEXTOS DE CONSENTIMIENTO
# =====================================
#
# Al cambiar un texto hay que subir su versión:
# los pacientes deberán aceptarlo de nuevo.
# Revisar con un abogado y un psicólogo antes de
# producción.

CONSENT_DOCUMENTS = {

    PlatformConsentTypeEnum.INFORMED_CONSENT: {
        "version": "1.0",
        "title": "Consentimiento informado de DEI",
        "content": (
            "DEI es un diario emocional de apoyo a tu "
            "proceso terapéutico. No reemplaza la "
            "atención de un profesional de salud mental "
            "y no realiza diagnósticos.\n\n"
            "DEI no es un servicio de emergencias. Tu "
            "profesional no revisa tus entradas en tiempo "
            "real. Si estás en peligro, llama a una línea "
            "de crisis o al número de emergencias.\n\n"
            "Solo los profesionales a los que otorgues "
            "consentimiento pueden ver tus entradas, y "
            "puedes revocarlo cuando quieras.\n\n"
            "Límites de la confidencialidad: si una "
            "entrada indica riesgo para tu vida o la de "
            "otras personas, DEI avisará a tus "
            "profesionales vinculados, y ellos podrán "
            "actuar según su deber profesional y la ley."
        ),
    },

    PlatformConsentTypeEnum.AI_PROCESSING: {
        "version": "1.0",
        "title": "Uso de inteligencia artificial",
        "content": (
            "DEI puede analizar tus entradas con "
            "inteligencia artificial para identificar "
            "emociones, nivel de riesgo y generar "
            "recomendaciones y resúmenes.\n\n"
            "Según la configuración del servicio, el "
            "texto o el audio se procesa en servidores "
            "propios de DEI (IA local) o se envía a "
            "Google Gemini, un servicio externo que "
            "puede procesar los datos fuera de tu país.\n\n"
            "Los resultados de la IA son orientativos y "
            "pueden equivocarse. Puedes retirar este "
            "consentimiento en cualquier momento; seguirás "
            "pudiendo escribir en tu diario sin análisis "
            "automático."
        ),
    },
}
