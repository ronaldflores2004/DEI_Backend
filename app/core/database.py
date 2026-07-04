from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.core.config import settings

# =====================================================
# Engine de SQLAlchemy
# =====================================================

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

# =====================================================
# Fábrica de sesiones
# =====================================================

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# =====================================================
# Clase base para todos los modelos ORM
# =====================================================

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Proporciona una sesión de base de datos por petición.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()