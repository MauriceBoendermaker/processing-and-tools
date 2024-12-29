"""
Drop and re-add is_deleted column

Revision ID: 5546e8ab362c
Revises: 95582c9d2e4c
Create Date: 2024-12-29 10:18:57.429612
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5546e8ab362c"
down_revision: Union[str, None] = "95582c9d2e4c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Drop the old is_deleted column (if it exists) and re-add a new is_deleted
    column with the correct default (0) and non-nullable constraint for each table.
    """

    tables = [
        "clients",
        "docks",
        "inventories",
        "item_groups",
        "item_lines",
        "item_types",
        "items",
        "locations",
        "orders",
        "shipments",
        "suppliers",
        "transfers",
        "warehouses",
    ]

    for table_name in tables:
        op.drop_column(table_name, "is_deleted")
        op.add_column(
            table_name,
            sa.Column(
                "is_deleted",
                sa.Boolean(),
                nullable=False,
                server_default="0"  # This ensures new rows default to 0 (False)
            )
        )


def downgrade() -> None:
    """
    Since you don't need a rollback, we'll do nothing here.
    If you needed to revert, you'd re-drop the column and re-add the old definition.
    """
    pass
