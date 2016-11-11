import sqlalchemy as sa


def unix_timestamp():
    """ Produces a BIGINT value of current UNIX timestamp """
    return sa.text('cast(EXTRACT(EPOCH FROM NOW()) as BIGINT)')


def int_pk():
    """ Used to add Integer primary key to the table """
    return (sa.Column('id', sa.Integer, primary_key=True), )


def timestamp():
    """ The function's purpose is to add `created_at` and `updated_at` columns
    to all tables.
    The values will be populated automatically on server side:
        - For `created_at` on INSERT;
        - For `updated_at` on INSERT and UPDATE.
    """
    return (
        sa.Column('created_at', sa.BigInteger,
                  default=unix_timestamp(),
                  server_default=unix_timestamp()),
        sa.Column('updated_at', sa.BigInteger,
                  default=unix_timestamp(),
                  server_default=unix_timestamp(),
                  onupdate=unix_timestamp(),
                  server_onupdate=unix_timestamp()),
    )


def base():
    """ The function returns base table mixin.
    It's used to add integer `id`, `created_at` and `updated_at` to all tables.
    """
    return int_pk() + timestamp()

