from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = '7943286daad9'
down_revision: Union[str, None] = '834405e7f7e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    inspector = Inspector.from_engine(op.get_bind())

    # Verifique se a tabela 'company' já existe
    if 'company' not in inspector.get_table_names():
        op.create_table(
            'company',
            sa.Column('id', sa.BigInteger, primary_key=True),
            sa.Column('cargo_criador', sa.String(255)),
            sa.Column('razao_social', sa.String(255)),
            sa.Column('nome_fantasia', sa.String(255)),
            sa.Column('cnpj', sa.String(18), unique=True),
            sa.Column('insc_estadual', sa.String(20)),
            sa.Column('insc_municipal', sa.String(20)),
            sa.Column('telefone', sa.String(15)),
            sa.Column('email', sa.String(255)),
            sa.Column('endereco', sa.String(255)),
            sa.Column('numero', sa.String(10)),
            sa.Column('complemento', sa.String(255)),
            sa.Column('bairro', sa.String(255)),
            sa.Column('cep', sa.String(10)),
            sa.Column('cidade', sa.String(255)),
            sa.Column('estado', sa.String(2)),
            sa.Column('pais', sa.String(50)),
        )

def downgrade() -> None:
    # Remova a tabela 'company'
    op.drop_table('company')
