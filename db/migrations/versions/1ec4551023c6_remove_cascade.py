"""remove cascade

Revision ID: 1ec4551023c6
Revises: 61b575fd02bd
Create Date: 2024-11-24 18:31:50.950802

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ec4551023c6'
down_revision: Union[str, None] = '61b575fd02bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('ingredient_recipe_associations_recipe_id_fkey', 'ingredient_recipe_associations', type_='foreignkey')
    op.create_foreign_key(None, 'ingredient_recipe_associations', 'recipes', ['recipe_id'], ['id'])
    op.drop_constraint('instructions_recipe_id_fkey', 'instructions', type_='foreignkey')
    op.create_foreign_key(None, 'instructions', 'recipes', ['recipe_id'], ['id'])
    op.drop_constraint('recipe_images_recipe_id_fkey', 'recipe_images', type_='foreignkey')
    op.create_foreign_key(None, 'recipe_images', 'recipes', ['recipe_id'], ['id'])
    op.drop_constraint('recipe_tag_recipe_associations_recipe_id_fkey', 'recipe_tag_recipe_associations', type_='foreignkey')
    op.create_foreign_key(None, 'recipe_tag_recipe_associations', 'recipes', ['recipe_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'recipe_tag_recipe_associations', type_='foreignkey')
    op.create_foreign_key('recipe_tag_recipe_associations_recipe_id_fkey', 'recipe_tag_recipe_associations', 'recipes', ['recipe_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'recipe_images', type_='foreignkey')
    op.create_foreign_key('recipe_images_recipe_id_fkey', 'recipe_images', 'recipes', ['recipe_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'instructions', type_='foreignkey')
    op.create_foreign_key('instructions_recipe_id_fkey', 'instructions', 'recipes', ['recipe_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'ingredient_recipe_associations', type_='foreignkey')
    op.create_foreign_key('ingredient_recipe_associations_recipe_id_fkey', 'ingredient_recipe_associations', 'recipes', ['recipe_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###