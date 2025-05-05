"""create token's user column

Revision ID: 6a5b15154bc6
Revises: 
Create Date: 2025-05-05 17:48:50.170384

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a5b15154bc6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('users', sa.Column('token', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'token')
    pass
