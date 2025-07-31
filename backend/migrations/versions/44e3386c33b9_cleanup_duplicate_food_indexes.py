"""cleanup_duplicate_food_indexes

Revision ID: 44e3386c33b9
Revises: 8e21735b3345
Create Date: 2025-07-31 20:23:19.547469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44e3386c33b9'
down_revision: Union[str, None] = '8e21735b3345'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Clean up duplicate food table indexes."""
    # Drop the old/duplicate indexes
    op.drop_index('ix_food_food_provider', table_name='food')  # old food_vendor index
    op.drop_index('ix_food_new_date', table_name='food')       # duplicate date index
    op.drop_index('ix_food_new_name', table_name='food')       # duplicate name index
    
    # Rename new_food_provider to proper food_vendor index
    op.drop_index('ix_food_new_food_provider', table_name='food')
    op.create_index('ix_food_food_vendor', 'food', ['food_vendor'], unique=False)


def downgrade() -> None:
    """Restore duplicate indexes."""
    # Restore the old indexes
    op.create_index('ix_food_food_provider', 'food', ['food_vendor'], unique=False)
    op.create_index('ix_food_new_date', 'food', ['date'], unique=False)
    op.create_index('ix_food_new_name', 'food', ['name'], unique=False)
    
    # Restore the old new_food_provider index
    op.drop_index('ix_food_food_vendor', table_name='food')
    op.create_index('ix_food_new_food_provider', 'food', ['food_vendor'], unique=False)
