"""empty message

Revision ID: 6357712f70c0
Revises: 
Create Date: 2017-02-24 11:22:28.848214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6357712f70c0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('adwordsGeo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('countryNumber', sa.String(length=100), nullable=True),
    sa.Column('countryName', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('adwordsGeo')
    # ### end Alembic commands ###
