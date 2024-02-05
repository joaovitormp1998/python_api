"""Updated ordens_servico table

Revision ID: 84ebf49eac5e
Revises: 8458cf5b84f3
Create Date: 2024-01-15 09:48:52.301984

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84ebf49eac5e'
down_revision: Union[str, None] = '8458cf5b84f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the optional stripe_pagamento_id column
    op.add_column('ordem_servico', sa.Column('stripe_pagamento_id', sa.String(255), nullable=True))


def downgrade() -> None:
    # Drop the stripe_pagamento_id column if it exists
    op.drop_column('ordem_servico', 'stripe_pagamento_id')