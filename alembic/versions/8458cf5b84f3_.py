"""empty message

Revision ID: 8458cf5b84f3
Revises: 800d87645141, 8ca1b5e0b699
Create Date: 2024-01-15 09:47:49.664301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8458cf5b84f3'
down_revision: Union[str, None] = ('800d87645141', '8ca1b5e0b699')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
