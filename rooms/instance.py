import asyncio
import aiohttp_jinja2
import jinja2
import json
import os
import aiohttp
from os import getenv
from aiohttp import web
from rooms.db.core.utils import get_db
from rooms.db.unit import action as unit_action
from rooms.db.room import action as room_action


class App(web.Application):
    def __init__(self, db=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if db:
            self.init_db(db)

    def configure(self, config):
        self['_config'] = config

    def init_db(self, engine):
        self['_db'] = engine

    @property
    def config(self):
        return self['_config']

    @property
    def db(self):
        return self['_db']


@aiohttp_jinja2.template('create_unit.html')
async def new_unit(request):
    return {'request': request}


@aiohttp_jinja2.template('units_list.html')
async def get_units(request):
    async with request.app.db.acquire() as conn:
        units = await unit_action.get_units(conn)
        return {'request': request, 'units': units}


def get_small_rooms_length(large_room_length):
    if large_room_length % 2 == 0:
        return (large_room_length / 2, ) * 2
    len1 = (large_room_length - 1) / 2
    len2 = len1 + 1
    return (len1, len2, )



def get_rooms(width, length):
    min_room_size = 80
    max_room_size = 1000
    unit_size = width * length
    if unit_size > max_room_size * 3 or unit_size < min_room_size * 3:
        raise ValueError('Wrong unit size')
    max_side = max(width, length)
    min_side = min(width, length)
    if max_side % 3 == 0:
        room_width = max_side / 3
        room_length = min_side
        return ((room_width, room_length), ) * 3
    elif max_side % 2 == 0:
        large_room_width = max_side / 2
        large_room_length = min_side
        small_rooms_width = large_room_width
    else:
        large_room_width = (max_side - 1) / 2
        large_room_length = min_side
        small_rooms_width = large_room_width + 1
    small_rooms_length = get_small_rooms_length(large_room_length)
    return (((large_room_width, large_room_length), ) +
            ((small_rooms_width, small_rooms_length[0]),
             (small_rooms_width, small_rooms_length[1])))


async def calculate_unit(request):
    width = int(request.GET['width'])
    length = int(request.GET['length'])
    try:
        rooms = get_rooms(width, length)
    except ValueError as e:
        raise web.HTTPBadRequest(reason=str(e))
    return web.Response(body=json.dumps(rooms).encode('utf-8'),
                        content_type='application/json')


async def create_unit(request):
    async with request.app.db.acquire() as conn:
        req_json = await request.json()
        unit_fields = {
            'name': req_json['name'],
            'width': req_json['width'],
            'length': req_json['length'],
        }
        unit = await unit_action.create(conn, **unit_fields)
        for r in req_json['rooms']:
            room = await room_action.create(conn, width=r[0], length=r[1],
                                            unit_id=unit['id'])
        unit_with_rooms = await unit_action.get_unit_with_rooms(
                conn, unit['id'])
    return web.json_response(unit_with_rooms, status=201)


def get_config():
    return {
        'DB': {
            'host': getenv('POSTGRES_HOST', '127.0.0.1'),
            'port': getenv('POSTGRES_PORT', 5432),
            'user': getenv('POSTGRES_USER', 'rooms'),
            'password': getenv('POSTGRES_PASSWORD', 'rooms'),
            'database': getenv('POSTGRES_DB', 'rooms'),
        },
    }


def create_loop():
    return asyncio.get_event_loop()


async def create_application(loop):
    config = get_config()
    db = await get_db(config['DB'])
    app = App(loop=loop)
    app.configure(config)
    app.init_db(db)

    curr_dir = os.path.dirname(os.path.realpath(__file__))
    tpl_dir = os.path.join(curr_dir, 'templates')
    static_dir = os.path.join(curr_dir, 'static')
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(tpl_dir))

    app.router.add_get('/units/new', new_unit, name='new_unit')
    app.router.add_get('/units/calculate', calculate_unit,
                        name='calculate_unit')
    app.router.add_post('/units', create_unit, name='create_unit')
    app.router.add_get('/units', get_units, name='get_units')
    app.router.add_static('/static/', static_dir, name='static')
    return app


loop = create_loop()
app = loop.run_until_complete(create_application(create_loop()))


if __name__ == '__main__':
    web.run_app(app)

