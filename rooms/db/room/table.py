import sqlalchemy as sa
from ..core import metadata
from ..core import table_mixin
from ..core.utils import foreign_key_column



room_table = sa.Table(
    'room',
    metadata,
    sa.Column('width', sa.Integer(), nullable=False),
    sa.Column('length', sa.Integer(), nullable=False),
    foreign_key_column('unit_id', 'unit.id', ondelete='CASCADE'),
    *table_mixin.base()
)


room_table.c.unit_id.nullable = False

