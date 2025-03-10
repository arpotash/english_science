"""add column word topic

Revision ID: 542fb34c2b52
Revises: 225815d1273c
Create Date: 2025-01-22 20:32:04.015484

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '542fb34c2b52'
down_revision: Union[str, None] = '225815d1273c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('word', sa.Column('topic', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('word', 'topic')
    # ### end Alembic commands ###
