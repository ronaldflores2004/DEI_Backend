import os

# La configuración se valida al importar, así que las
# variables deben existir antes de cargar la app.
os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("SECRET_KEY", "x" * 32)
# Clave Fernet válida solo para tests (cifrado en reposo).
os.environ.setdefault("DATA_ENCRYPTION_KEYS", "M2Q4ZTFjYjJhZjVkNGU3ZjkwYjFjM2Q1ZTdmOWExYjM=")
os.environ.setdefault("AI_PROVIDER_CHAIN", "OLLAMA,GEMINI,FAKE")
os.environ.setdefault("OLLAMA_BASE_URL", "http://ollama.test:11434")
os.environ.setdefault("OLLAMA_MODEL", "llama3.1:8b")
os.environ.setdefault("WHISPER_API_URL", "http://whisper.test:8000")
