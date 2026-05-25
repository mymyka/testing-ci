"""hello world

Revision ID: 0a4ebe2e3784
Revises: 
Create Date: 2026-05-26 00:05:53.243590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0a4ebe2e3784'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
