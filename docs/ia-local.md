# IA local (Ollama + Whisper)

El backend prueba los proveedores de IA en el orden de `AI_PROVIDER_CHAIN`.
Con `OLLAMA,GEMINI,FAKE` usa primero la IA local, recurre a Gemini solo si
la local falla y, como último recurso, al proveedor simulado.
Así se gastan tokens de Gemini únicamente cuando la laptop con la IA está apagada
o responde algo inválido.

| Tarea | Proveedores |
|---|---|
| Análisis emocional | Ollama, Gemini, Fake |
| Resumen semanal | Ollama, Gemini, Fake |
| Recomendaciones | Ollama, Fake (Gemini aún no implementado) |
| Transcripción de audio | Whisper por HTTP (`WHISPER_API`) o en proceso (`LOCAL`) |

## Topología

```
ThinkPad (backend FastAPI)  ──HTTP──▶  Nitro 5 (Ollama :11434, Whisper :8000)
```

## 1. En la Nitro 5 (máquina con la IA)

Ollama solo escucha en `localhost` por defecto. Para que la ThinkPad pueda llegar:

```bash
# Windows (PowerShell): variable de entorno del usuario y reiniciar Ollama
setx OLLAMA_HOST 0.0.0.0

# Linux
sudo systemctl edit ollama   # Environment="OLLAMA_HOST=0.0.0.0"

ollama pull llama3.1:8b
```

Para Whisper, levanta un servidor compatible con la API de OpenAI
(`POST /v1/audio/transcriptions`), por ejemplo
[speaches / faster-whisper-server](https://github.com/speaches-ai/speaches):

(revisa su README para el comando de Docker con GPU). Si en la Nitro ya tienes
Whisper como script de Python, basta con envolverlo en un endpoint con ese contrato:
recibe `file`, `model` y `language` como multipart y responde `{"text": "..."}`.

Abre los puertos 11434 y 8000 en el firewall solo para la red local.

## 2. En la ThinkPad (backend)

Copia `.env.example` a `.env` y ajusta la IP de la Nitro:

```
AI_PROVIDER_CHAIN=OLLAMA,GEMINI,FAKE
OLLAMA_BASE_URL=http://<ip-de-la-nitro>:11434
OLLAMA_MODEL=llama3.1:8b
TRANSCRIPTION_PROVIDER=WHISPER_API
WHISPER_API_URL=http://<ip-de-la-nitro>:8000
```

## 3. Verificar

Con un usuario ADMIN:

```
GET /health/ai
```

Responde si Ollama es alcanzable, si el modelo está descargado,
si hay clave de Gemini y qué cadena de proveedores está activa.
En `logs/dei_backend.log` queda registrado qué proveedor resolvió cada tarea.

## Tests

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

Los tests simulan Ollama y Whisper; no necesitan la Nitro encendida ni gastan tokens.
