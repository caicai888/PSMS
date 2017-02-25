"""empty message

Revision ID: d8b757403f98
Revises: 84eb8836148a
Create Date: 2017-02-24 14:21:54.917924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8b757403f98'
down_revision = '84eb8836148a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('adwords', sa.Column('profit', sa.Float(), nullable=True))
    op.add_column('adwords', sa.Column('revenue', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('adwords', 'revenue')
    op.drop_column('adwords', 'profit')
    # ### end Alembic commands ###