"""add settings table

Revision ID: 1e9d5d3800e7
Revises: 0a4ebe2e3784
Create Date: 2026-05-26 00:14:31.348253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '1e9d5d3800e7'
down_revision: Union[str, None] = '0a4ebe2e3784'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
