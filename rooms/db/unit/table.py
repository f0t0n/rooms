import sqlalchemy as sa
from ..core import metadata
from ..core import table_mixin



unit_table = sa.Table(
    'unit',
    metadata,
    sa.Column('name', sa.String(255), nullable=False),
    sa.Column('width', sa.Integer(), nullable=False),
    sa.Column('length', sa.Integer(), nullable=False),
    *table_mixin.base()
)

