"""segunda migracao

Revision ID: 8da231da1ef5
Revises: 03f7cf2c09fd
Create Date: 2025-07-24 10:50:25.326632

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8da231da1ef5'
down_revision: Union[str, Sequence[str], None] = '03f7cf2c09fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
