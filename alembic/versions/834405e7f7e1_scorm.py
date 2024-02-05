from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = '834405e7f7e1'
down_revision: Union[str, None] = '16f78363d402'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    inspector = Inspector.from_engine(op.get_bind())

    # Verifique se a tabela 'scorm' já existe
    if 'scorm' not in inspector.get_table_names():
        op.create_table(
            'scorm',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('tenant_id', sa.String(length=255, collation='utf8mb4_unicode_ci'), sa.ForeignKey('tenants.id'), nullable=False),
            sa.Column('s3_key', sa.String(50), nullable=False),
        )

def downgrade() -> None:
    # Remova a tabela 'scorm'
    op.drop_table('scorm')
