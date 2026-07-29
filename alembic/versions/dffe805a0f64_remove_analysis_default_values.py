"""remove analysis default values

Revision ID: dffe805a0f64
Revises: 541f7458c034
Create Date: 2026-07-29 17:53:32.017452

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dffe805a0f64'
down_revision: Union[str, Sequence[str], None] = '541f7458c034'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove temporary server defaults."""

    op.alter_column(
        "emotional_analyses",
        "provider",
        server_default=None,
        existing_type=sa.String(),
        existing_nullable=False,
    )

    op.alter_column(
        "emotional_analyses",
        "model",
        server_default=None,
        existing_type=sa.String(),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Restore temporary server defaults."""

    op.alter_column(
        "emotional_analyses",
        "provider",
        server_default="UNKNOWN",
        existing_type=sa.String(),
        existing_nullable=False,
    )

    op.alter_column(
        "emotional_analyses",
        "model",
        server_default="UNKNOWN",
        existing_type=sa.String(),
        existing_nullable=False,
    )