"""create recordings table

Revision ID: 291d46413e86
Revises:
Create Date: 2026-10-15 09:01:17.878631

"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "291d46413e86"
down_revision: str | None = None
branch_labels: str | None = None
depends_on: str | None = None

RECORDING_STATUS = (
    "UPLOADED",
    "TRANSCRIBING",
    "TRANSCRIBED",
    "CHUNKING",
    "SUMMARIZING",
    "COMPLETED",
    "FAILED",
)


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "recordings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("filename", sa.String(), nullable=False),
        sa.Column("storage_path", sa.String(), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM(*RECORDING_STATUS, name="recording_status"),
            nullable=False,
        ),
        sa.Column("error_message", sa.String(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("recordings")
    sa.Enum(name="recording_status").drop(op.get_bind(), checkfirst=True)
