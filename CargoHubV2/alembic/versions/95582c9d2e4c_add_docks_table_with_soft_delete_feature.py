"""Add docks table with soft delete support

Revision ID: 95582c9d2e4c
Revises: e1f93f49957c
Create Date: 2024-12-17 11:48:13.015284

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95582c9d2e4c'
down_revision: Union[str, None] = 'e1f93f49957c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create docks table with soft delete (is_deleted as the last column)
    op.create_table(
        'docks',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('warehouse_id', sa.Integer(), sa.ForeignKey('warehouses.id', ondelete="CASCADE"), nullable=False),
        sa.Column('code', sa.String(50), unique=True, nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.text("False"))
    )

    # Existing changes for soft delete in other tables
    op.alter_column('clients', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text("'False'"))
    op.alter_column('inventories', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text("'False'"))
    op.alter_column('item_groups', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text("'False'"))
    op.alter_column('item_lines', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text("'False'"))
    op.alter_column('item_types', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text("'False'"))
    op.alter_column('items', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text("'False'"))
    op.alter_column('locations', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text("'False'"))
    op.alter_column('orders', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text("'False'"))
    op.alter_column('shipments', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text("'False'"))
    op.alter_column('suppliers', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text("'False'"))
    op.alter_column('transfers', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text("'False'"))
    op.drop_index('ix_transfers_reference', table_name='transfers')
    op.create_unique_constraint(None, 'transfers', ['reference'])
    op.alter_column('warehouses', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text("'False'"))


def downgrade() -> None:
    # Drop docks table
    op.drop_table('docks')

    # Revert the existing soft delete changes for other tables
    op.alter_column('warehouses', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text("'False'"))
    op.drop_constraint(None, 'transfers', type_='unique')
    op.create_index('ix_transfers_reference', 'transfers', ['reference'], unique=1)
    op.alter_column('transfers', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text("'False'"))
    op.alter_column('suppliers', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text("'False'"))
    op.alter_column('shipments', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text("'False'"))
    op.alter_column('orders', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text("'False'"))
    op.alter_column('locations', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text("'False'"))
    op.alter_column('items', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text("'False'"))
    op.alter_column('item_types', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text("'False'"))
    op.alter_column('item_lines', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text("'False'"))
    op.alter_column('item_groups', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text("'False'"))
    op.alter_column('inventories', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text("'False'"))
    op.alter_column('clients', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text("'False'"))
