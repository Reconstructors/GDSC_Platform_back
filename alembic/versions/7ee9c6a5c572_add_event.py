"""add Event

Revision ID: 7ee9c6a5c572
Revises: 7f826a5f8e6f
Create Date: 2024-02-18 14:49:10.265563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ee9c6a5c572'
down_revision: Union[str, None] = '7f826a5f8e6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
