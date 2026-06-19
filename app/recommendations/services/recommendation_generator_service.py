def generate_recommendation(
    primary_emotion: str
):

    if primary_emotion == "Ansiedad":
        return {
            "title": "Gestión de ansiedad",
            "content": (
                "Has mostrado señales de ansiedad. "
                "Intenta identificar las situaciones "
                "que la desencadenan durante el día."
            )
        }

    if primary_emotion == "Tristeza":
        return {
            "title": "Reflexión emocional",
            "content": (
                "Dedica unos minutos a escribir "
                "qué eventos han influido en tu estado emocional."
            )
        }

    if primary_emotion == "Estrés":
        return {
            "title": "Manejo del estrés",
            "content": (
                "Considera realizar pausas breves "
                "durante actividades exigentes."
            )
        }

    return {
        "title": "Bienestar emocional",
        "content": (
            "Continúa registrando tus emociones "
            "para identificar patrones personales."
        )
    }