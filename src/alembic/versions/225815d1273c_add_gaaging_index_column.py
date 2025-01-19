"""add gaaging index column

Revision ID: 225815d1273c
Revises: 3cb63a3499bc
Create Date: 2025-01-16 13:04:34.168311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '225815d1273c'
down_revision: Union[str, None] = '3cb63a3499bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('unit', sa.Column('gaaging_idx', sa.Float(), nullable=True))
    op.add_column('unit', sa.Column('diversity_idx', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('unit', 'gaaging_idx')
    op.drop_column('unit', 'diversity_idx')
    # ### end Alembic commands ###
