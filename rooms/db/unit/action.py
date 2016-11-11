from .table import unit_table
from ..room.table import room_table

from sqlalchemy import select
from sqlalchemy import join
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import text


async def create(conn, **fields):
    query = (unit_table.insert()
             .values(**fields)
             .returning(*unit_table.columns))
    res = await conn.execute(query)
    unit = await res.first()
    return dict(unit)


async def get_unit_with_rooms(conn, unit_id):
    j = join(unit_table, room_table,
             and_(unit_table.c.id == room_table.c.unit_id,
                  unit_table.c.id == unit_id))
    rooms_agg = func.json_agg(text(room_table.name)).label('rooms')
    query = (select((unit_table, rooms_agg, ))
             .select_from(j)
             .group_by(unit_table.c.id)
             .order_by(unit_table.c.created_at))
    res = await conn.execute(query)
    return dict((await res.first()))


async def get_units(conn):
    j = join(unit_table, room_table,
             unit_table.c.id == room_table.c.unit_id)
    rooms_agg = func.json_agg(text(room_table.name)).label('rooms')
    query = (select((unit_table, rooms_agg, ))
             .select_from(j)
             .group_by(unit_table.c.id)
             .order_by(unit_table.c.created_at))
    res = await conn.execute(query)
    return list(map(dict, await res.fetchall()))

