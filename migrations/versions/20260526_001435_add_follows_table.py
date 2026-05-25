"""add follows table

Revision ID: de20c3bcacb9
Revises: 0a4ebe2e3784
Create Date: 2026-05-26 00:14:35.109056

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'de20c3bcacb9'
down_revision: Union[str, None] = '0a4ebe2e3784'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
