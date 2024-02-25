"""add Event

Revision ID: 34c184deb3ad
Revises: 7ee9c6a5c572
Create Date: 2024-02-18 14:52:53.739719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34c184deb3ad'
down_revision: Union[str, None] = '7ee9c6a5c572'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
