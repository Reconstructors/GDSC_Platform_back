"""modify User

Revision ID: ffc75fdc3ca7
Revises: 34c184deb3ad
Create Date: 2024-02-18 15:57:31.964363

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffc75fdc3ca7'
down_revision: Union[str, None] = '34c184deb3ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
