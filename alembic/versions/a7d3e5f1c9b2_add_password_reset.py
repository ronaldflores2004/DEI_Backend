"""add password reset codes and token version

Revision ID: a7d3e5f1c9b2
Revises: f4c8d1a6b3e9
Create Date: 2026-11-19 20:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7d3e5f1c9b2'
down_revision: Union[str, Sequence[str], None] = 'f4c8d1a6b3e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Recuperación de contraseña y cierre de sesiones."""

    # Los tokens actuales no llevan "ver" y cuentan
    # como versión 0: nadie pierde la sesión al migrar.
    op.add_column(
        "users",
        sa.Column(
            "token_version",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.create_table(
        "password_reset_codes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("code_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("failed_attempts", sa.Integer(), nullable=False),
        sa.Column("consumed_at", sa.DateTime(), nullable=True),
        sa.Column("requested_ip", sa.String(length=45), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_password_reset_codes_id",
        "password_reset_codes",
        ["id"],
    )

    op.create_index(
        "ix_password_reset_codes_user_created",
        "password_reset_codes",
        ["user_id", "created_at"],
    )


def downgrade() -> None:

    op.drop_index(
        "ix_password_reset_codes_user_created",
        table_name="password_reset_codes",
    )

    op.drop_index(
        "ix_password_reset_codes_id",
        table_name="password_reset_codes",
    )

    op.drop_table("password_reset_codes")

    op.drop_column("users", "token_version")
