"""initial schema

Crea las tablas base del proyecto tal como existían antes
de que se empezara a usar Alembic (cuando se creaban con
Base.metadata.create_all). Las migraciones siguientes
agregan índices, columnas y restricciones encima.

Revision ID: 0f2a6c1d9b3e
Revises:
Create Date: 2026-10-28 01:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0f2a6c1d9b3e"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('message', sa.String(length=1000), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('is_read', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_id'), 'notifications', ['id'], unique=False)
    op.create_table('patient_profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=False),
    sa.Column('gender', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_patient_profiles_id'), 'patient_profiles', ['id'], unique=False)
    op.create_table('professional_profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('license_number', sa.String(length=100), nullable=False),
    sa.Column('specialties', sa.String(length=500), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('verified_by_admin', sa.Integer(), nullable=True),
    sa.Column('verified_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_professional_profiles_id'), 'professional_profiles', ['id'], unique=False)
    op.create_table('consents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('professional_id', sa.Integer(), nullable=False),
    sa.Column('granted', sa.Boolean(), nullable=True),
    sa.Column('granted_at', sa.DateTime(), nullable=True),
    sa.Column('revoked_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patient_profiles.id'], ),
    sa.ForeignKeyConstraint(['professional_id'], ['professional_profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_consents_id'), 'consents', ['id'], unique=False)
    op.create_table('emotional_entries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('entry_type', sa.String(length=20), nullable=False),
    sa.Column('text_content', sa.Text(), nullable=True),
    sa.Column('audio_path', sa.String(length=500), nullable=True),
    sa.Column('is_archived', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patient_profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_emotional_entries_id'), 'emotional_entries', ['id'], unique=False)
    op.create_table('link_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('professional_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patient_profiles.id'], ),
    sa.ForeignKeyConstraint(['professional_id'], ['professional_profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_link_requests_id'), 'link_requests', ['id'], unique=False)
    op.create_table('patient_professionals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('professional_id', sa.Integer(), nullable=False),
    sa.Column('sharing_mode', sa.String(length=50), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('ended_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patient_profiles.id'], ),
    sa.ForeignKeyConstraint(['professional_id'], ['professional_profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_patient_professionals_id'), 'patient_professionals', ['id'], unique=False)
    op.create_table('therapy_sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('professional_id', sa.Integer(), nullable=False),
    sa.Column('session_date', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patient_profiles.id'], ),
    sa.ForeignKeyConstraint(['professional_id'], ['professional_profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_therapy_sessions_id'), 'therapy_sessions', ['id'], unique=False)
    op.create_table('audio_transcriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('entry_id', sa.Integer(), nullable=False),
    sa.Column('transcription_text', sa.Text(), nullable=False),
    sa.Column('provider', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['entry_id'], ['emotional_entries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audio_transcriptions_id'), 'audio_transcriptions', ['id'], unique=False)
    op.create_table('clinical_notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('professional_id', sa.Integer(), nullable=False),
    sa.Column('note', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['professional_id'], ['professional_profiles.id'], ),
    sa.ForeignKeyConstraint(['session_id'], ['therapy_sessions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clinical_notes_id'), 'clinical_notes', ['id'], unique=False)
    op.create_table('emotional_analyses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('entry_id', sa.Integer(), nullable=False),
    sa.Column('primary_emotion', sa.String(length=100), nullable=True),
    sa.Column('emotion_intensity', sa.String(length=50), nullable=True),
    sa.Column('risk_level', sa.String(length=50), nullable=True),
    sa.Column('analysis_json', sa.JSON(), nullable=False),
    sa.Column('analyzed_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['entry_id'], ['emotional_entries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_emotional_analyses_id'), 'emotional_analyses', ['id'], unique=False)
    op.create_table('patient_recommendations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('analysis_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('source', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['analysis_id'], ['emotional_analyses.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patient_profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_patient_recommendations_id'), 'patient_recommendations', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('patient_recommendations')
    op.drop_table('emotional_analyses')
    op.drop_table('clinical_notes')
    op.drop_table('audio_transcriptions')
    op.drop_table('therapy_sessions')
    op.drop_table('patient_professionals')
    op.drop_table('link_requests')
    op.drop_table('emotional_entries')
    op.drop_table('consents')
    op.drop_table('professional_profiles')
    op.drop_table('patient_profiles')
    op.drop_table('notifications')
    op.drop_table('users')
