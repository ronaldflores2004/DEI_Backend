"""enforce unique active clinical relationships

Revision ID: 541f7458c034
Revises: af9ae5e39c35
Create Date: 2026-07-29 01:23:45.841289

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "541f7458c034"
down_revision: Union[str, Sequence[str], None] = "af9ae5e39c35"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Enforce one active consent and relationship per pair."""

    op.create_index(
        "uq_active_consent_patient_professional",
        "consents",
        ["patient_id", "professional_id"],
        unique=True,
        postgresql_where=sa.text("granted = true"),
    )

    op.create_index(
        "uq_active_patient_professional",
        "patient_professionals",
        ["patient_id", "professional_id"],
        unique=True,
        postgresql_where=sa.text("active = true"),
    )


def downgrade() -> None:
    """Remove active clinical uniqueness constraints."""

    op.drop_index(
        "uq_active_patient_professional",
        table_name="patient_professionals",
        postgresql_where=sa.text("active = true"),
    )

    op.drop_index(
        "uq_active_consent_patient_professional",
        table_name="consents",
        postgresql_where=sa.text("granted = true"),
    )