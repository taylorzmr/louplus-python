"""empty message

Revision ID: 70e7047da162
Revises: ed06324566ee
Create Date: 2017-12-05 13:22:46.186576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70e7047da162'
down_revision = 'ed06324566ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_disable', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_disable')
    # ### end Alembic commands ###
