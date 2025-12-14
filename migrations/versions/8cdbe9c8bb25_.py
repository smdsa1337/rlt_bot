"""empty message

Revision ID: 8cdbe9c8bb25
Revises: 
Create Date: 2025-12-14 01:58:20.369790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cdbe9c8bb25'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('CREATE SCHEMA IF NOT EXISTS rlt_bot')
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('DROP SCHEMA IF EXISTS rlt_bot CASCADE')
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp"')
