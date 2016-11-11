"""Add unit width and length

Revision ID: c207e9d525ca
Revises: b816ee70ec83
Create Date: 2016-11-11 21:15:26.953582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c207e9d525ca'
down_revision = 'b816ee70ec83'
branch_labels = None
depends_on = None

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('unit', sa.Column('length', sa.Integer(), nullable=False))
    op.add_column('unit', sa.Column('width', sa.Integer(), nullable=False))
    op.drop_column('unit', 'size')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('unit', sa.Column('size', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('unit', 'width')
    op.drop_column('unit', 'length')
    ### end Alembic commands ###
