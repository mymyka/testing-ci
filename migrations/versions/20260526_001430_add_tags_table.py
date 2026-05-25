"""add tags table

Revision ID: 3945a7668e14
Revises: 0a4ebe2e3784
Create Date: 2026-05-26 00:14:30.062714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '3945a7668e14'
down_revision: Union[str, None] = '0a4ebe2e3784'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
