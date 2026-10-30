"""add platform consents

Revision ID: 7c3e9a1f2b4d
Revises: dffe805a0f64
Create Date: 2026-10-30 12:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c3e9a1f2b4d'
down_revision: Union[str, Sequence[str], None] = 'dffe805a0f64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Crea la tabla de consentimientos hacia la plataforma."""

    op.create_table(
        "platform_consents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("consent_type", sa.String(length=50), nullable=False),
        sa.Column("version", sa.String(length=20), nullable=False),
        sa.Column("granted_at", sa.DateTime(), nullable=False),
        sa.Column("revoked_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["patient_id"],
            ["patient_profiles.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_platform_consents_id",
        "platform_consents",
        ["id"],
    )

    op.create_index(
        "ix_platform_consents_patient_type",
        "platform_consents",
        ["patient_id", "consent_type"],
    )


def downgrade() -> None:
    """Elimina la tabla de consentimientos hacia la plataforma."""

    op.drop_index(
        "ix_platform_consents_patient_type",
        table_name="platform_consents",
    )

    op.drop_index(
        "ix_platform_consents_id",
        table_name="platform_consents",
    )

    op.drop_table("platform_consents")
