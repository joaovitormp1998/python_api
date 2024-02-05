from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = '16f78363d402'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Verifique se a tabela de grupos já existe
    inspector = Inspector.from_engine(op.get_bind())
    if 'groups' not in inspector.get_table_names():
        # Crie a tabela de grupos
        op.create_table(
            'groups',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('name', sa.String(255), nullable=False),
            sa.Column('description', sa.String(512)),
        )

    # Verifique se a coluna `group_id` já existe na tabela de usuários
    if 'group_id' not in [col['name'] for col in inspector.get_columns('users')]:
        # Adicione a coluna `group_id` na tabela de usuários
        op.add_column('users', sa.Column('group_id', sa.Integer, sa.ForeignKey('groups.id')))

def downgrade() -> None:
    # Remova a coluna `group_id` da tabela de usuários
    op.drop_column('users', 'group_id')

    # Remova a tabela de grupos de usuário
    op.drop_table('groups')
