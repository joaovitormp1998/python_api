from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, DateTime, String, BigInteger, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.sql import func
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = 'c942446633ea'
down_revision: Union[str, None] = '9d16edeba346'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    inspector = Inspector.from_engine(op.get_bind())

    # Verifique se a tabela 'chamados' já existe
    if 'chamados' not in inspector.get_table_names():
        op.create_table(
            'chamados',
            Column('id', BIGINT(unsigned=True), primary_key=True),
            Column('created_by', BIGINT(unsigned=True), ForeignKey('users.id'), nullable=False),
            Column('descricao', String(255), nullable=False),
            Column('tipo', String(255), nullable=False),
            Column('updated_at', DateTime, default=func.now(), onupdate=func.now(), nullable=False),
            Column('created_at', DateTime, default=func.now(), nullable=False)
        )

def downgrade() -> None:
    # Remova a tabela 'chamados'
    op.drop_table('chamados')
