from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = '9d16edeba346'
down_revision: Union[str, None] = 'cf22cb946686'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    inspector = Inspector.from_engine(op.get_bind())

    # Verifique se a tabela 'ordem_servico' já existe
    if 'ordem_servico' not in inspector.get_table_names():
        op.create_table(
            'ordem_servico',
            sa.Column('id', sa.BigInteger, primary_key=True),
            sa.Column('company_id', sa.BigInteger, sa.ForeignKey('company.id'), nullable=False),
            sa.Column('status', sa.String(length=255), nullable=False),
            sa.Column('created_at', sa.DateTime, default=sa.func.now(), nullable=False),
            sa.Column('updated_at', sa.DateTime, default=sa.func.now(), nullable=False),
        )

    # Verifique se a tabela 'ordem_servico_product_invoice' já existe
    if 'ordem_servico_product_invoice' not in inspector.get_table_names():
        op.create_table(
            'ordem_servico_product_invoice',
            sa.Column('ordem_servico_id', sa.BigInteger, sa.ForeignKey('ordem_servico.id'), nullable=False),
            sa.Column('product_invoice_id', sa.Integer, sa.ForeignKey('product_invoice.id'), nullable=False),
        )

def downgrade():
    # Remova as tabelas 'ordem_servico_product_invoice' e 'ordem_servico'
    op.drop_table('ordem_servico_product_invoice')
    op.drop_table('ordem_servico')
