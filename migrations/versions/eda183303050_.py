"""empty message

Revision ID: eda183303050
Revises: 0705173c9425
Create Date: 2018-02-27 23:10:11.559966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eda183303050'
down_revision = '0705173c9425'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('loggedinuser',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password', sa.String(length=64), nullable=True),
    sa.Column('logged_in', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('business',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('category', sa.String(length=64), nullable=True),
    sa.Column('location', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_business_name'), 'business', ['name'], unique=True)
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('review_summary', sa.String(length=64), nullable=True),
    sa.Column('review_description', sa.String(length=150), nullable=True),
    sa.Column('star_rating', sa.String(length=10), nullable=True),
    sa.Column('business_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['business.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_review_review_summary'), 'review', ['review_summary'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_review_review_summary'), table_name='review')
    op.drop_table('review')
    op.drop_index(op.f('ix_business_name'), table_name='business')
    op.drop_table('business')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_table('loggedinuser')
    # ### end Alembic commands ###
