"""Add posts table

Revision ID: 60d14339b058
Revises: 
Create Date: 2022-03-19 10:13:03.804013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60d14339b058'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), primary_key = True, nullable = False),
                    sa.Column('title', sa.String(), nullable = False),
                    sa.Column('content', sa.String(), nullable = False),
                    sa.Column('published', sa.Boolean(), server_default = 'True', nullable = False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone = True), nullable = False, 
                    server_default = sa.sql.expression.text('now()'))
                    )

def downgrade():
    op.drop_table('posts')