"""modify User

Revision ID: 84f01c90b4a6
Revises: ffc75fdc3ca7
Create Date: 2024-02-18 16:04:48.082688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84f01c90b4a6'
down_revision: Union[str, None] = 'ffc75fdc3ca7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
