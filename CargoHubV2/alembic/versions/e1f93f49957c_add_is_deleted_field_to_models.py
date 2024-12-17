"""Add is_deleted field to models

Revision ID: e1f93f49957c
Revises: 18a2dd8935ed
Create Date: 2024-12-17 11:07:50.597239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1f93f49957c'
down_revision: Union[str, None] = '18a2dd8935ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### Add is_deleted column with default value False ###
    op.add_column('clients', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='False'))
    op.add_column('inventories', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='False'))
    op.add_column('item_groups', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='False'))
    op.add_column('item_lines', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='False'))
    op.add_column('item_types', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='False'))
    op.add_column('items', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='False'))
    op.add_column('locations', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='False'))
    op.add_column('orders', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='False'))
    op.add_column('shipments', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='False'))
    op.add_column('suppliers', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='False'))
    op.add_column('transfers', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='False'))
    op.add_column('warehouses', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='False'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### Drop the is_deleted column ###
    op.drop_column('warehouses', 'is_deleted')
    op.drop_column('transfers', 'is_deleted')
    op.drop_column('suppliers', 'is_deleted')
    op.drop_column('shipments', 'is_deleted')
    op.drop_column('orders', 'is_deleted')
    op.drop_column('locations', 'is_deleted')
    op.drop_column('items', 'is_deleted')
    op.drop_column('item_types', 'is_deleted')
    op.drop_column('item_lines', 'is_deleted')
    op.drop_column('item_groups', 'is_deleted')
    op.drop_column('inventories', 'is_deleted')
    op.drop_column('clients', 'is_deleted')
    # ### end Alembic commands ###
