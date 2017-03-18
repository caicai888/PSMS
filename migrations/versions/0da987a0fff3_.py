"""empty message

Revision ID: 0da987a0fff3
Revises: 90fe0e520492
Create Date: 2017-03-13 10:56:39.247913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0da987a0fff3'
down_revision = '90fe0e520492'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('optimization',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('simple', sa.String(length=100), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('createdTime', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'campaignRelations', sa.Column('optName', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'campaignRelations', 'optName')
    op.drop_table('optimization')
    # ### end Alembic commands ###