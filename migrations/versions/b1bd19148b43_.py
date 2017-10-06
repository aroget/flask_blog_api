"""empty message

Revision ID: b1bd19148b43
Revises: 61a7d6834031
Create Date: 2017-10-04 11:55:23.318085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1bd19148b43'
down_revision = '61a7d6834031'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('is_disabled', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_disabled')
    op.drop_column('users', 'is_active')
    # ### end Alembic commands ###
