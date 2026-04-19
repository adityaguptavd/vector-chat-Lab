"""add soft delete and timestamps to all tables

Revision ID: de61ff2678a1
Revises: 1a54d32acf47
Create Date: 2026-04-19 10:19:58.974321

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de61ff2678a1'
down_revision: Union[str, Sequence[str], None] = '1a54d32acf47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op
import sqlalchemy as sa


def upgrade():
    # USERS
    op.add_column("users", sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("users", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("users", sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.add_column("users", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))

    # DOCUMENTS
    op.add_column("documents", sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("documents", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("documents", sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.add_column("documents", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))

    # CHAT_MESSAGES
    op.add_column("chat_messages", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("chat_messages", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))

    # CHAT_SESSIONS
    op.add_column("chat_sessions", sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("chat_sessions", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))


def downgrade():
    # USERS
    op.drop_column("users", "updated_at")
    op.drop_column("users", "created_at")
    op.drop_column("users", "deleted_at")
    op.drop_column("users", "is_deleted")

    # DOCUMENTS
    op.drop_column("documents", "updated_at")
    op.drop_column("documents", "created_at")
    op.drop_column("documents", "deleted_at")
    op.drop_column("documents", "is_deleted")

    # CHAT_MESSAGES
    op.drop_column("chat_messages", "updated_at")
    op.drop_column("chat_messages", "deleted_at")

    # CHAT_SESSIONS
    op.drop_column("chat_sessions", "deleted_at")
    op.drop_column("chat_sessions", "is_deleted")
