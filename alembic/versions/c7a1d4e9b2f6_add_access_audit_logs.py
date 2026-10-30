"""add access audit logs

Revision ID: c7a1d4e9b2f6
Revises: b5e8c3a7d9f2
Create Date: 2026-10-30 13:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7a1d4e9b2f6'
down_revision: Union[str, Sequence[str], None] = 'b5e8c3a7d9f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Crea la tabla de auditoría de accesos."""

    op.create_table(
        "access_audit_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("professional_id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["professional_id"],
            ["professional_profiles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["patient_id"],
            ["patient_profiles.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_access_audit_logs_id",
        "access_audit_logs",
        ["id"],
    )

    op.create_index(
        "ix_access_audit_patient_created",
        "access_audit_logs",
        ["patient_id", "created_at"],
    )


def downgrade() -> None:
    """Elimina la tabla de auditoría de accesos."""

    op.drop_index(
        "ix_access_audit_patient_created",
        table_name="access_audit_logs",
    )

    op.drop_index(
        "ix_access_audit_logs_id",
        table_name="access_audit_logs",
    )

    op.drop_table("access_audit_logs")
