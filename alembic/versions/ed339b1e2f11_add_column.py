"""ADD COLUMN

Revision ID: ed339b1e2f11
Revises: 7943286daad9
Create Date: 2023-12-18 11:16:37.178588

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed339b1e2f11'
down_revision: Union[str, None] = '7943286daad9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adicione a coluna 'created_by' somente se não existir
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    columns = inspector.get_columns('company')

    has_created_by = any(column['name'] == 'created_by' for column in columns)

    if not has_created_by:
        # Adiciona a coluna 'created_by' com tipo BIGINT e a torna nullable
        op.execute('ALTER TABLE company ADD COLUMN created_by BIGINT UNSIGNED NULL')

        # Adicione a restrição da chave estrangeira apenas se a coluna foi criada
        op.execute('ALTER TABLE company ADD CONSTRAINT fk_created_by_users FOREIGN KEY (created_by) REFERENCES users (id)')


def downgrade() -> None:
    # Remova as restrições ao desfazer a migração
    op.execute('ALTER TABLE company DROP FOREIGN KEY fk_created_by_users')
    op.execute('ALTER TABLE company DROP COLUMN created_by')
