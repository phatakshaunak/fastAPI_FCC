"""Add users table

Revision ID: 15b82625cc4a
Revises: 60d14339b058
Create Date: 2022-03-19 12:21:31.349924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15b82625cc4a'
down_revision = '60d14339b058'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), primary_key = True, nullable = False),
                    sa.Column('email', sa.String(), nullable = False, unique = True),
                    sa.Column('password', sa.String(), nullable = False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone = True), nullable = False, 
                    server_default = sa.sql.expression.text('now()'))
                    )

def downgrade():
    op.drop_table('users')

'''class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
'''