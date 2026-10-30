import os


# =====================================
# LÍNEAS DE CRISIS POR PAÍS
# =====================================
#
# Verificar los números con las autoridades de
# salud de cada país antes de salir a producción:
# cambian con el tiempo.
#
# El país se elige con CRISIS_COUNTRY (código ISO
# de dos letras, BO por defecto). Si el país no
# está en la lista, solo se muestra el mensaje
# general.

CRISIS_LINES = {
    # Fuentes: UNICEF Bolivia (Familia Segura) y el
    # aviso de viaje de Canadá (policía y ambulancia),
    # consultados en octubre de 2026.
    "BO": [
        {
            "name": (
                "Familia Segura, línea gratuita y "
                "confidencial (todos los días, de 6:00 "
                "a 24:00)"
            ),
            "phone": "800 11 30 40"
        },
        {
            "name": "Familia Segura por WhatsApp",
            "phone": "77797667"
        },
        {
            "name": "Policía (emergencias)",
            "phone": "110"
        },
        {
            "name": "Ambulancia en La Paz",
            "phone": "165"
        },
    ],
    "PE": [
        {
            "name": "Línea 113 Salud (opción 5, salud mental)",
            "phone": "113"
        },
    ],
    "MX": [
        {
            "name": "Línea de la Vida",
            "phone": "800 911 2000"
        },
    ],
    "ES": [
        {
            "name": "Línea 024 de atención a la conducta suicida",
            "phone": "024"
        },
    ],
    "US": [
        {
            "name": "988 Suicide & Crisis Lifeline",
            "phone": "988"
        },
    ],
}

CRISIS_MESSAGE = (
    "Lo que escribiste nos importa. Si sientes que "
    "podrías hacerte daño o estás en peligro, busca "
    "ayuda ahora: llama a una línea de crisis o al "
    "número de emergencias de tu país, o acude a la "
    "emergencia más cercana. DEI no es un servicio "
    "de emergencias y tu profesional puede no ver "
    "este mensaje de inmediato."
)


def get_crisis_resources() -> dict:

    country = os.getenv(
        "CRISIS_COUNTRY",
        "BO"
    ).upper()

    return {
        "message": CRISIS_MESSAGE,
        "lines": CRISIS_LINES.get(country, []),
    }
