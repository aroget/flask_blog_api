"""empty message

Revision ID: de2b8601602d
Revises: 2e98bcbecafc
Create Date: 2017-10-04 10:19:28.226817

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'de2b8601602d'
down_revision = '2e98bcbecafc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('firstname', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('lastname', sa.String(length=120), nullable=True))
    op.drop_column('user', 'first_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('first_name', mysql.VARCHAR(length=120), nullable=True))
    op.drop_column('user', 'lastname')
    op.drop_column('user', 'firstname')
    # ### end Alembic commands ###
