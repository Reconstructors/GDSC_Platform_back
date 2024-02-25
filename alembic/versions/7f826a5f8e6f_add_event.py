"""add Event

Revision ID: 7f826a5f8e6f
Revises: 2503196a38cd
Create Date: 2024-02-18 14:47:50.195459

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f826a5f8e6f'
down_revision: Union[str, None] = '2503196a38cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
