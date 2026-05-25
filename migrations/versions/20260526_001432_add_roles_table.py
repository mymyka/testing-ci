"""add roles table

Revision ID: 413741cb6d46
Revises: 0a4ebe2e3784
Create Date: 2026-05-26 00:14:32.671827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '413741cb6d46'
down_revision: Union[str, None] = '0a4ebe2e3784'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
