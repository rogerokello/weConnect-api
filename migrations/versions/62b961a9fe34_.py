"""empty message

Revision ID: 62b961a9fe34
Revises: 6d43ee721b48
Create Date: 2018-02-27 19:43:41.514210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62b961a9fe34'
down_revision = '6d43ee721b48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('logged_in', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'logged_in')
    # ### end Alembic commands ###
