"""add last_activity_at field in table chat_sessions

Revision ID: 5e90d8692d0b
Revises: 2bdfdb87b44f
Create Date: 2026-04-19 12:12:17.922464

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e90d8692d0b'
down_revision: Union[str, Sequence[str], None] = '2bdfdb87b44f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. Add as NULLABLE first
    op.add_column(
        "chat_sessions",
        sa.Column(
            "last_activity_at",
            sa.DateTime(timezone=True),
            nullable=True
        )
    )

    # 2. Backfill existing rows
    op.execute("""
        UPDATE chat_sessions
        SET last_activity_at = created_at
        WHERE last_activity_at IS NULL
    """)

    # 3. Make it NOT NULL
    op.alter_column(
        "chat_sessions",
        "last_activity_at",
        nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("chat_sessions", "last_activity_at")
