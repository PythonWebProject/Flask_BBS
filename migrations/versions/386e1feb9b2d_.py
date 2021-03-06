"""empty message

Revision ID: 386e1feb9b2d
Revises: dd9320e96540
Create Date: 2020-07-03 16:53:49.871517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '386e1feb9b2d'
down_revision = 'dd9320e96540'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('commenter_id', sa.String(length=40), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('is_delete', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['commenter_id'], ['front_user.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    # ### end Alembic commands ###
