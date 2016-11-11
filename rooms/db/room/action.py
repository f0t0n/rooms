from .table import room_table


async def create(conn, **fields):
    query = (room_table.insert()
             .values(**fields)
             .returning(*room_table.columns))
    res = await conn.execute(query)
    return dict(await res.first())

