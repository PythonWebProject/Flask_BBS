"""empty message

Revision ID: c1dfed7157ce
Revises: 48e7bfc163da
Create Date: 2020-06-27 09:36:17.992262

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c1dfed7157ce'
down_revision = '48e7bfc163da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cms_role_user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cms_role_user',
    sa.Column('cms_role_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('cms_user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('cms_role_id', 'cms_user_id'),
    mysql_default_charset='utf8',
    mysql_engine='MyISAM'
    )
    # ### end Alembic commands ###
