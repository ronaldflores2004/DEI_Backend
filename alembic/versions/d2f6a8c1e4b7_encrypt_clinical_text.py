"""encrypt clinical text at rest

Revision ID: d2f6a8c1e4b7
Revises: c7a1d4e9b2f6
Create Date: 2026-10-30 23:30:00.000000

Requiere DATA_ENCRYPTION_KEYS configurada: cifra
las filas existentes con la clave principal.

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.shared.security.field_encryption import (
    TOKEN_PREFIX,
    encrypt_text,
    decrypt_text,
)


# revision identifiers, used by Alembic.
revision: str = 'd2f6a8c1e4b7'
down_revision: Union[str, Sequence[str], None] = 'c7a1d4e9b2f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# tabla, columna
ENCRYPTED_COLUMNS = [
    ("emotional_entries", "text_content"),
    ("audio_transcriptions", "transcription_text"),
    ("emotional_analyses", "analysis_json"),
    ("clinical_notes", "note"),
    ("patient_recommendations", "content"),
]


def _transform(table: str, column: str, encrypt: bool) -> None:

    connection = op.get_bind()

    rows = connection.execute(
        sa.text(
            f"SELECT id, {column} FROM {table} "
            f"WHERE {column} IS NOT NULL"
        )
    ).fetchall()

    for row_id, value in rows:

        is_encrypted = value.startswith(TOKEN_PREFIX)

        if encrypt == is_encrypted:
            continue

        connection.execute(
            sa.text(
                f"UPDATE {table} SET {column} = :value "
                f"WHERE id = :id"
            ),
            {
                "value": (
                    encrypt_text(value)
                    if encrypt
                    else decrypt_text(value)
                ),
                "id": row_id,
            },
        )


def upgrade() -> None:
    """Cifra el texto clínico existente."""

    # El JSON cifrado se guarda como texto.
    op.alter_column(
        "emotional_analyses",
        "analysis_json",
        type_=sa.Text(),
        existing_type=sa.JSON(),
        postgresql_using="analysis_json::text",
    )

    for table, column in ENCRYPTED_COLUMNS:
        _transform(table, column, encrypt=True)


def downgrade() -> None:
    """Vuelve a texto plano el texto clínico."""

    for table, column in ENCRYPTED_COLUMNS:
        _transform(table, column, encrypt=False)

    op.alter_column(
        "emotional_analyses",
        "analysis_json",
        type_=sa.JSON(),
        existing_type=sa.Text(),
        postgresql_using="analysis_json::json",
    )
