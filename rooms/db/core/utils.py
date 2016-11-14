import sqlalchemy as sa
from aiopg.sa import create_engine



def foreign_key_column(column_name, foreign_column, **foreign_key_options):
    """ Helper function for foreign key definition.
    Example of usage:

    ```
    from ..core.utils import foreign_key_column
    media_table = sa.Table(
        'post',
        metadata,
        # ...
        foreign_key_column('author_id', 'user.id', ondelete='CASCADE')
        # ...
    )
    ```
    """
    fk_name = '{}__{}_fkey'.format(column_name,
                                   foreign_column.replace('.', '_'))
    fk_options = {'name': fk_name, **foreign_key_options}
    return sa.Column(column_name, sa.Integer(),
                     sa.ForeignKey(foreign_column, **fk_options))


# aiopg stuff

async def get_db(config: dict):
    return await create_engine(**config)


async def close_engine(app):
    app.logger.info('Gonna close DB connection...')
    app.db.close()
    await app.db.wait_closed()
    app.logger.info('DB conneciton is {}closed.'
                    .format('' if app.db.closed else 'not '))

