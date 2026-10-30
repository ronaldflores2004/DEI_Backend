"""add recommendation review

Revision ID: e3b7c9d2f5a8
Revises: d2f6a8c1e4b7
Create Date: 2026-10-30 23:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3b7c9d2f5a8'
down_revision: Union[str, Sequence[str], None] = 'd2f6a8c1e4b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Revisión de recomendaciones por el profesional."""

    # Las recomendaciones existentes ya las vio el
    # paciente: quedan aprobadas.
    op.add_column(
        "patient_recommendations",
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="APPROVED",
        ),
    )

    op.alter_column(
        "patient_recommendations",
        "status",
        server_default=None,
        existing_type=sa.String(length=20),
        existing_nullable=False,
    )

    op.add_column(
        "patient_recommendations",
        sa.Column(
            "reviewed_by_professional_id",
            sa.Integer(),
            sa.ForeignKey(
                "professional_profiles.id",
                name="fk_recommendations_reviewed_by",
            ),
            nullable=True,
        ),
    )

    op.add_column(
        "patient_recommendations",
        sa.Column("reviewed_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    """Elimina la revisión de recomendaciones."""

    op.drop_column("patient_recommendations", "reviewed_at")

    op.drop_constraint(
        "fk_recommendations_reviewed_by",
        "patient_recommendations",
        type_="foreignkey",
    )

    op.drop_column(
        "patient_recommendations",
        "reviewed_by_professional_id",
    )

    op.drop_column("patient_recommendations", "status")
