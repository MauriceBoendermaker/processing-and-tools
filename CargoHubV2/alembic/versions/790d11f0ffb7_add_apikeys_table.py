"""Add APIKeys table

Revision ID: 790d11f0ffb7
Revises: 23568d0fd535
Create Date: 2024-11-16 23:47:34.377809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision: str = '790d11f0ffb7'
down_revision: Union[str, None] = '23568d0fd535'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('api_keys', sa.Column('role', sa.String(), nullable=False))
    op.add_column('api_keys', sa.Column('permissions', sqlite.JSON(), nullable=False))
    op.drop_column('api_keys', 'expires_at')
    op.drop_column('api_keys', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('api_keys', sa.Column('user_id', sa.INTEGER(), nullable=False))
    op.add_column('api_keys', sa.Column('expires_at', sa.DATETIME(), nullable=True))
    op.drop_column('api_keys', 'permissions')
    op.drop_column('api_keys', 'role')
    # ### end Alembic commands ###