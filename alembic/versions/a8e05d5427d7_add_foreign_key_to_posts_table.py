"""add foreign key to posts table

Revision ID: a8e05d5427d7
Revises: 15b82625cc4a
Create Date: 2022-03-19 12:29:43.652360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8e05d5427d7'
down_revision = '15b82625cc4a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable = False))
    op.create_foreign_key('posts_users_fk', source_table = "posts", referent_table = "users", 
                          local_cols = ['user_id'], remote_cols = ['id'], ondelete = 'CASCADE')

def downgrade():
    op.drop_constrain('posts_users_fk', table_name = 'posts')
    op.drop_column('posts', 'user_id')
