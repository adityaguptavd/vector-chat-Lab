"""remove server defaults

Revision ID: 2bdfdb87b44f
Revises: de61ff2678a1
Create Date: 2026-04-19 10:23:22.646285

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2bdfdb87b44f'
down_revision: Union[str, Sequence[str], None] = 'de61ff2678a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "users", "created_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=None
    )
    op.alter_column(
        "users", "updated_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=None
    )

    op.alter_column(
        "documents", "created_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=None
    )
    op.alter_column(
        "documents", "updated_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=None
    )

    op.alter_column(
        "chat_messages", "created_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=None
    )
    op.alter_column(
        "chat_messages", "updated_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=None
    )

    op.alter_column(
        "chat_sessions", "created_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=None
    )
    op.alter_column(
        "chat_sessions", "updated_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=None
    )
    


def downgrade():
    op.alter_column(
        "users", "created_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.func.now()
    )
    op.alter_column(
        "users", "updated_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.func.now()
    )

    op.alter_column(
        "documents", "created_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.func.now()
    )
    op.alter_column(
        "documents", "updated_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.func.now()
    )

    op.alter_column(
        "chat_messages", "created_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.func.now()
    )
    op.alter_column(
        "chat_messages", "updated_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.func.now()
    )

    op.alter_column(
        "chat_sessions", "created_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.func.now()
    )
    op.alter_column(
        "chat_sessions", "updated_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.func.now()
    )
