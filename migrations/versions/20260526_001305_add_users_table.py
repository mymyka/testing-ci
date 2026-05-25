"""add users table

Revision ID: 532f80caf01e
Revises: 0a4ebe2e3784
Create Date: 2026-05-26 00:13:05.673472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '532f80caf01e'
down_revision: Union[str, None] = '0a4ebe2e3784'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
