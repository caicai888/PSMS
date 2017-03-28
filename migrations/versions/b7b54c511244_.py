"""empty message

Revision ID: b7b54c511244
Revises: caf060c54320
Create Date: 2017-03-26 18:21:55.866715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7b54c511244'
down_revision = 'caf060c54320'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('campaignRelations', sa.Column('account_name', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('campaignRelations', 'account_name')
    # ### end Alembic commands ###