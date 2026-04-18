"""add full_name to users

Revision ID: 1a54d32acf47
Revises: 
Create Date: 2026-04-18 14:25:39.760742

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a54d32acf47'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "users",
        sa.Column("full_name", sa.String(length=255), nullable=True),
    )


def downgrade():
    op.drop_column("users", "full_name")
