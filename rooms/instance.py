import asyncio
import aiohttp_jinja2
import jinja2
import os
import aiohttp
from aiohttp import web
from rooms.db.core.utils import get_db
from os import getenv


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


def get_rooms(unit_size):
    min_room_size = 80
    max_room_size = 1000
    if unit_size > max_room_size * 3 or unit_size < min_room_size * 3:
        raise ValueError('Wrong unit size')

async def calculate_unit(request):
    print(request.GET['size'])
    return web.Response()


async def create_unit(request):
    return web.HTTPCreated()


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
    # app.router.add_get('/units', get_units, name='get_units')
    app.router.add_static('/static/', static_dir, name='static')
    return app


loop = create_loop()
app = loop.run_until_complete(create_application(create_loop()))


if __name__ == '__main__':
    web.run_app(app)

