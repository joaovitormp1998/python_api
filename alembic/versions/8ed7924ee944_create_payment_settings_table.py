from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = '8ed7924ee944'
down_revision: Union[str, None] = 'c942446633ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    inspector = Inspector.from_engine(op.get_bind())

    # Verifique se a tabela 'payment_settings' já existe
    if 'payment_settings' not in inspector.get_table_names():
        op.create_table(
            'payment_settings',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('descricao_na_fatura', sa.String(255), nullable=False),
            sa.Column('parcelamento_cartao_recorrente', sa.String(255)),
            sa.Column('parcelamento_cartao', sa.String(255)),
            sa.Column('parcelamento_boleto', sa.String(255)),
            sa.Column('dias_vencimento_boleto', sa.Integer),
            sa.Column('dias_bloqueio_curso', sa.Integer),
            sa.Column('dias_bloqueio_extensao', sa.Integer),
            sa.Column('valor_minimo_parcela', sa.Float),
            sa.Column('taxa_imposto', sa.Float),
            sa.Column('habilitar_solicitacao_bolsa', sa.Boolean),
            sa.Column('aceitar_boleto_bancario', sa.Boolean),
            sa.Column('aceitar_pix', sa.Boolean),
            sa.Column('aceitar_cartao_credito', sa.Boolean),
            sa.Column('aceitar_cartao_credito_recorrente', sa.Boolean),
            # ... outros campos do paymentSettings
        )

def downgrade():
    # Remova a tabela 'payment_settings'
    op.drop_table('payment_settings')
