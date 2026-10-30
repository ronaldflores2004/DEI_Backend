import httpx


def install_fake_http(monkeypatch, handler):
    """
    Reemplaza httpx.post/httpx.get por un transporte
    simulado para no depender de Ollama ni Whisper reales.
    """

    client = httpx.Client(
        transport=httpx.MockTransport(handler)
    )

    def fake_post(url, **kwargs):
        kwargs.pop("timeout", None)
        return client.post(url, **kwargs)

    def fake_get(url, **kwargs):
        kwargs.pop("timeout", None)
        return client.get(url, **kwargs)

    monkeypatch.setattr(httpx, "post", fake_post)
    monkeypatch.setattr(httpx, "get", fake_get)


def ollama_reply(content: str) -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "message": {
                "role": "assistant",
                "content": content
            }
        }
    )


def unreachable(request: httpx.Request) -> httpx.Response:
    raise httpx.ConnectError(
        "connection refused",
        request=request
    )
