"""add reports table

Revision ID: cbc8e689fac0
Revises: 0a4ebe2e3784
Create Date: 2026-05-26 00:14:34.734160

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'cbc8e689fac0'
down_revision: Union[str, None] = '0a4ebe2e3784'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
