"""tabela assinatura atualizacao

Revision ID: ad36d8328f0a
Revises: 1b658bbbe4a3
Create Date: 2025-07-24 10:54:58.730628

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad36d8328f0a'
down_revision: Union[str, Sequence[str], None] = '1b658bbbe4a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assinaturas', sa.Column('nome', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('assinaturas', 'nome')
    # ### end Alembic commands ###
