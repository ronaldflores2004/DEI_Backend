"""add sharing choice to link requests

Revision ID: 9d4b2e6f8a1c
Revises: 7c3e9a1f2b4d
Create Date: 2026-10-30 12:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d4b2e6f8a1c'
down_revision: Union[str, Sequence[str], None] = '7c3e9a1f2b4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """El paciente elige qué historial comparte."""

    # Las solicitudes existentes conservan el
    # comportamiento anterior (todo el historial).
    op.add_column(
        "link_requests",
        sa.Column(
            "sharing_mode",
            sa.String(length=50),
            nullable=False,
            server_default="FULL_HISTORY",
        ),
    )

    op.alter_column(
        "link_requests",
        "sharing_mode",
        server_default=None,
        existing_type=sa.String(length=50),
        existing_nullable=False,
    )

    op.add_column(
        "link_requests",
        sa.Column("share_from", sa.DateTime(), nullable=True),
    )

    op.add_column(
        "patient_professionals",
        sa.Column("share_from", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    """Elimina la elección de historial compartido."""

    op.drop_column("patient_professionals", "share_from")

    op.drop_column("link_requests", "share_from")

    op.drop_column("link_requests", "sharing_mode")
