"""
Message: merge all heads
Revision ID: 9c7763e2cd29
Revises: 532f80caf01e, 387df4d89f92, f4db2baeef03, 9c7ded85dd76, 4d928ce1b431, 72e5c47f3755, 3945a7668e14, 7f1f78b21823, f6ef25dbf791, 1e9d5d3800e7, 915a7bf08a01, 413741cb6d46, 66cfe6f7fe9c, 346942ca8ee4, 1536a43464ab, 2edda29882e3, 22b4607c7b29, cbc8e689fac0, 93bd0f9bd4da, 8d13ba65b533, de20c3bcacb9, 5199741d2e41
Create Date: 2026-05-26 00:18:15.378216
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '9c7763e2cd29'
down_revision: Union[str, None, Sequence[str]] = ('532f80caf01e', '387df4d89f92', 'f4db2baeef03', '9c7ded85dd76', '4d928ce1b431', '72e5c47f3755', '3945a7668e14', '7f1f78b21823', 'f6ef25dbf791', '1e9d5d3800e7', '915a7bf08a01', '413741cb6d46', '66cfe6f7fe9c', '346942ca8ee4', '1536a43464ab', '2edda29882e3', '22b4607c7b29', 'cbc8e689fac0', '93bd0f9bd4da', '8d13ba65b533', 'de20c3bcacb9', '5199741d2e41')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
