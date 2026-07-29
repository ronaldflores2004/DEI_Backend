"""enforce unique analysis and transcription per entry

Revision ID: af9ae5e39c35
Revises: d226ac7620a0
Create Date: 2026-07-29 00:57:56.653383

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "af9ae5e39c35"
down_revision: Union[str, Sequence[str], None] = "d226ac7620a0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Enforce one transcription and one analysis per entry."""

    op.create_unique_constraint(
        "uq_audio_transcriptions_entry_id",
        "audio_transcriptions",
        ["entry_id"],
    )

    op.drop_index(
        "ix_emotional_analysis_entry",
        table_name="emotional_analyses",
    )

    op.create_unique_constraint(
        "uq_emotional_analyses_entry_id",
        "emotional_analyses",
        ["entry_id"],
    )


def downgrade() -> None:
    """Restore previous schema."""

    op.drop_constraint(
        "uq_emotional_analyses_entry_id",
        "emotional_analyses",
        type_="unique",
    )

    op.create_index(
        "ix_emotional_analysis_entry",
        "emotional_analyses",
        ["entry_id"],
        unique=False,
    )

    op.drop_constraint(
        "uq_audio_transcriptions_entry_id",
        "audio_transcriptions",
        type_="unique",
    )