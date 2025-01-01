"""
Baseline (Add only is_deleted columns, nothing else)
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = "3fc1e7f8868a"  # keep your generated revision ID
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('clients', sa.Column(
        'is_deleted', sa.Boolean(), server_default='0', nullable=False))
    op.add_column('inventories', sa.Column(
        'is_deleted', sa.Boolean(), server_default='0', nullable=False))
    op.add_column('item_groups', sa.Column(
        'is_deleted', sa.Boolean(), server_default='0', nullable=False))
    op.add_column('item_lines', sa.Column(
        'is_deleted', sa.Boolean(), server_default='0', nullable=False))
    op.add_column('item_types', sa.Column(
        'is_deleted', sa.Boolean(), server_default='0', nullable=False))
    op.add_column('items', sa.Column('is_deleted', sa.Boolean(),
                  server_default='0', nullable=False))
    op.add_column('locations', sa.Column(
        'is_deleted', sa.Boolean(), server_default='0', nullable=False))
    op.add_column('orders', sa.Column('is_deleted', sa.Boolean(),
                  server_default='0', nullable=False))
    op.add_column('shipments', sa.Column(
        'is_deleted', sa.Boolean(), server_default='0', nullable=False))
    op.add_column('suppliers', sa.Column(
        'is_deleted', sa.Boolean(), server_default='0', nullable=False))
    op.add_column('transfers', sa.Column(
        'is_deleted', sa.Boolean(), server_default='0', nullable=False))
    op.add_column('warehouses', sa.Column(
        'is_deleted', sa.Boolean(), server_default='0', nullable=False))


def downgrade() -> None:
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
