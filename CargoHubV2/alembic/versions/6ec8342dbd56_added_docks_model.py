"""Added docks model

Revision ID: 6ec8342dbd56
Revises: 3fc1e7f8868a
Create Date: 2025-01-01 22:34:50.379440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ec8342dbd56'
down_revision: Union[str, None] = '3fc1e7f8868a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create docks table
    op.create_table(
        'docks',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('warehouse_id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), server_default='0', nullable=False),
        sa.ForeignKeyConstraint(['warehouse_id'], ['warehouses.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_docks_code'), 'docks', ['code'], unique=True)
    op.create_index(op.f('ix_docks_id'), 'docks', ['id'], unique=False)
    op.create_index(op.f('ix_docks_warehouse_id'), 'docks', ['warehouse_id'], unique=False)

def downgrade() -> None:
    # Drop docks table and its indexes
    op.drop_index(op.f('ix_docks_warehouse_id'), table_name='docks')
    op.drop_index(op.f('ix_docks_id'), table_name='docks')
    op.drop_index(op.f('ix_docks_code'), table_name='docks')
    op.drop_table('docks')
