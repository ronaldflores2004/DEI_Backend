"""add risk alerts

Revision ID: b5e8c3a7d9f2
Revises: 9d4b2e6f8a1c
Create Date: 2026-10-30 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5e8c3a7d9f2'
down_revision: Union[str, Sequence[str], None] = '9d4b2e6f8a1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Crea la tabla de alertas de riesgo con seguimiento."""

    op.create_table(
        "risk_alerts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("professional_id", sa.Integer(), nullable=False),
        sa.Column("analysis_id", sa.Integer(), nullable=False),
        sa.Column("risk_level", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("seen_at", sa.DateTime(), nullable=True),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
        sa.Column("resolution_note", sa.String(length=1000), nullable=True),
        sa.ForeignKeyConstraint(
            ["patient_id"],
            ["patient_profiles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["professional_id"],
            ["professional_profiles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["analysis_id"],
            ["emotional_analyses.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_risk_alerts_id",
        "risk_alerts",
        ["id"],
    )

    op.create_index(
        "ix_risk_alerts_professional_status",
        "risk_alerts",
        ["professional_id", "status"],
    )

    op.create_index(
        "uq_risk_alert_analysis_professional",
        "risk_alerts",
        ["analysis_id", "professional_id"],
        unique=True,
    )


def downgrade() -> None:
    """Elimina la tabla de alertas de riesgo."""

    op.drop_index(
        "uq_risk_alert_analysis_professional",
        table_name="risk_alerts",
    )

    op.drop_index(
        "ix_risk_alerts_professional_status",
        table_name="risk_alerts",
    )

    op.drop_index(
        "ix_risk_alerts_id",
        table_name="risk_alerts",
    )

    op.drop_table("risk_alerts")
