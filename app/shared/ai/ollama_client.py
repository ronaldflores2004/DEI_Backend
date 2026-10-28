import json
import logging

import httpx

from app.core.config import (
    settings
)

from app.shared.exceptions.ai_provider_exception import (
    AIProviderException
)


logger = logging.getLogger(__name__)


class OllamaClient:
    """
    Cliente HTTP para el servidor Ollama.

    Ollama puede correr en otra máquina de la red
    (por ejemplo la laptop con GPU). Para eso, en esa
    máquina se debe iniciar con OLLAMA_HOST=0.0.0.0
    y aquí apuntar OLLAMA_BASE_URL a su IP.

    Cualquier fallo (red, timeout, respuesta inválida)
    se convierte en AIProviderException para que la
    cadena de proveedores pase al siguiente.
    """

    @staticmethod
    def generate(
        prompt: str,
        json_output: bool = False,
        model: str | None = None,
        temperature: float = 0.2,
    ) -> str:

        payload = {
            "model": model or settings.OLLAMA_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }

        if json_output:
            payload["format"] = "json"

        try:

            response = httpx.post(
                f"{settings.OLLAMA_BASE_URL}/api/chat",
                json=payload,
                timeout=settings.OLLAMA_TIMEOUT_SECONDS
            )

            response.raise_for_status()

            content = (
                response.json()["message"]["content"]
            )

        except (
            httpx.HTTPError,
            KeyError,
            TypeError,
            ValueError,
        ) as e:

            logger.warning(
                "Ollama no respondió correctamente: %s",
                e
            )

            raise AIProviderException(
                "Ollama no está disponible."
            ) from e

        content = (content or "").strip()

        if not content:
            raise AIProviderException(
                "Ollama devolvió una respuesta vacía."
            )

        return content

    @staticmethod
    def generate_json(
        prompt: str,
        model: str | None = None,
    ) -> dict:

        content = OllamaClient.generate(
            prompt=prompt,
            json_output=True,
            model=model
        )

        try:

            data = json.loads(content)

        except json.JSONDecodeError as e:

            raise AIProviderException(
                "Ollama devolvió JSON inválido."
            ) from e

        if not isinstance(data, dict):
            raise AIProviderException(
                "Ollama devolvió un JSON inesperado."
            )

        return data

    @staticmethod
    def health() -> dict:
        """
        Verifica si Ollama responde y si el
        modelo configurado está descargado.
        """

        try:

            response = httpx.get(
                f"{settings.OLLAMA_BASE_URL}/api/tags",
                timeout=5
            )

            response.raise_for_status()

            models = [
                item.get("name")
                for item in response.json().get("models", [])
            ]

        except (
            httpx.HTTPError,
            ValueError,
        ) as e:

            return {
                "reachable": False,
                "base_url": settings.OLLAMA_BASE_URL,
                "model": settings.OLLAMA_MODEL,
                "model_available": False,
                "error": str(e)
            }

        configured = settings.OLLAMA_MODEL

        model_available = any(
            name == configured
            or name == f"{configured}:latest"
            for name in models
        )

        return {
            "reachable": True,
            "base_url": settings.OLLAMA_BASE_URL,
            "model": configured,
            "model_available": model_available,
            "error": None
        }
