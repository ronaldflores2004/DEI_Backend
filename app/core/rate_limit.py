import math
import threading
import time

from collections import defaultdict, deque

from fastapi import HTTPException, Request


class RateLimiter:
    """
    Límite de solicitudes por IP con ventana deslizante,
    en memoria del proceso.

    Con varios workers o servidores cada uno lleva su
    propia cuenta; el límite por cuenta de usuario de la
    recuperación de contraseña sí vive en la base de
    datos y es global.
    """

    def __init__(
        self,
        name: str,
        max_requests: int,
        window_seconds: int
    ):
        self.name = name
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: dict[str, deque] = defaultdict(deque)
        self._lock = threading.Lock()

    def hit(self, key: str) -> float | None:
        """
        Registra una solicitud. Devuelve None si se
        permite, o los segundos que faltan para poder
        volver a intentar.
        """

        now = time.monotonic()

        with self._lock:

            hits = self._hits[key]

            while hits and now - hits[0] >= self.window_seconds:
                hits.popleft()

            if len(hits) >= self.max_requests:
                return self.window_seconds - (now - hits[0])

            hits.append(now)

            return None

    def reset(self) -> None:

        with self._lock:
            self._hits.clear()

    def __call__(self, request: Request) -> None:
        """
        Dependencia de FastAPI.
        """

        client_ip = (
            request.client.host
            if request.client
            else "unknown"
        )

        retry_after = self.hit(client_ip)

        if retry_after is not None:
            raise HTTPException(
                status_code=429,
                detail=(
                    "Demasiadas solicitudes. "
                    "Intenta de nuevo más tarde."
                ),
                headers={
                    "Retry-After": str(
                        max(1, math.ceil(retry_after))
                    )
                }
            )
