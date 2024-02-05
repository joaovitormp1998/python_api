from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8ca1b5e0b699'
down_revision: Union[str, None] = '8ed7924ee944'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column('payment_settings', sa.Column('gateway_id', sa.String(length=255), nullable=True))
    op.add_column('payment_settings', sa.Column('gateway_configuration', sa.JSON(), nullable=True))

def downgrade():
    op.drop_column('payment_settings', 'gateway_id')
    op.drop_column('payment_settings', 'gateway_configuration')
