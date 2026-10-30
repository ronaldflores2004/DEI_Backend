"""add crisis lines and system settings

Revision ID: f4c8d1a6b3e9
Revises: e3b7c9d2f5a8
Create Date: 2026-10-31 00:10:00.000000

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4c8d1a6b3e9'
down_revision: Union[str, Sequence[str], None] = 'e3b7c9d2f5a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Líneas iniciales de Bolivia. El administrador
# puede editarlas o desactivarlas desde el panel.
BOLIVIA_LINES = [
    (None, "Familia Segura, línea gratuita (6:00 a 24:00)", "800 11 30 40", 1),
    (None, "Familia Segura por WhatsApp", "77797667", 2),
    (None, "Policía (emergencias)", "110", 3),
    ("La Paz", "Ambulancia", "165", 4),
]


def upgrade() -> None:
    """Líneas de crisis y ajustes gestionados por el admin."""

    crisis_lines = op.create_table(
        "crisis_lines",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("country_code", sa.String(length=2), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_crisis_lines_id",
        "crisis_lines",
        ["id"],
    )

    op.create_index(
        "ix_crisis_lines_country_active",
        "crisis_lines",
        ["country_code", "is_active"],
    )

    now = datetime.utcnow()

    op.bulk_insert(
        crisis_lines,
        [
            {
                "country_code": "BO",
                "city": city,
                "name": name,
                "phone": phone,
                "sort_order": order,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            }
            for city, name, phone, order in BOLIVIA_LINES
        ],
    )

    op.create_table(
        "system_settings",
        sa.Column("key", sa.String(length=100), nullable=False),
        sa.Column("value", sa.String(length=1000), nullable=False),
        sa.Column("updated_by_user_id", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["updated_by_user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("key"),
    )


def downgrade() -> None:
    """Elimina líneas de crisis y ajustes del admin."""

    op.drop_table("system_settings")

    op.drop_index(
        "ix_crisis_lines_country_active",
        table_name="crisis_lines",
    )

    op.drop_index(
        "ix_crisis_lines_id",
        table_name="crisis_lines",
    )

    op.drop_table("crisis_lines")
