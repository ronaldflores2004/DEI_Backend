import logging

from collections.abc import Callable
from typing import TypeVar

from app.shared.ai.runtime_settings import (
    get_ai_provider_chain
)

from app.shared.exceptions.ai_provider_exception import (
    AIProviderException
)


logger = logging.getLogger(__name__)

ProviderT = TypeVar("ProviderT")
ResultT = TypeVar("ResultT")


class AIProviderChain:
    """
    Ejecuta una tarea de IA probando los proveedores
    en orden (AI_PROVIDER_CHAIN) hasta que uno responda.

    Ejemplo con OLLAMA,GEMINI,FAKE:
    primero la IA local, si falla Gemini y como
    último recurso el proveedor simulado.
    """

    @staticmethod
    def run(
        task: str,
        get_provider: Callable[[str], ProviderT],
        call: Callable[[ProviderT], ResultT],
        chain: list[str] | None = None,
    ) -> ResultT:

        chain = chain or get_ai_provider_chain()

        last_error: AIProviderException | None = None

        for name in chain:

            try:

                provider = get_provider(name)

                result = call(provider)

            except AIProviderException as e:

                logger.warning(
                    "Proveedor %s falló en '%s': %s",
                    name,
                    task,
                    e
                )

                last_error = e

                continue

            logger.info(
                "Tarea '%s' resuelta por %s",
                task,
                name
            )

            return result

        raise AIProviderException(
            f"Ningún proveedor de IA pudo completar '{task}'."
        ) from last_error
