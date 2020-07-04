"""empty message

Revision ID: 73fb9beae472
Revises: b18839d4793f
Create Date: 2020-06-29 19:32:01.969257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73fb9beae472'
down_revision = 'b18839d4793f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cms_board',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('is_delete', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cms_board')
    # ### end Alembic commands ###