from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = 'cf22cb946686'
down_revision: Union[str, None] = 'ed339b1e2f11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    inspector = Inspector.from_engine(op.get_bind())

    # Verifique se a tabela 'product_invoice' já existe
    if 'product_invoice' not in inspector.get_table_names():
        op.create_table(
            'product_invoice',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('categoria', sa.String(length=50), index=True),  # Adjust the length as needed
            sa.Column('nome', sa.String(length=255), index=True),      # Adjust the length as needed
            sa.Column('unidade_de_medida', sa.String(length=50)),      # Adjust the length as needed
            sa.Column('valor', sa.DECIMAL(precision=10, scale=2)),     # Adjust precision and scale as needed
        )

def downgrade():
    # Remova a tabela 'product_invoice'
    op.drop_table('product_invoice')
