from alembic import context
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from dotenv import load_dotenv
from os import getenv

load_dotenv()

SSL = getenv('DB_SSL')
PROTOCOL = getenv('DB_CONNECTION')
DRIVER = 'mysqlconnector'
USERNAME = getenv('DB_USERNAME')
PASSWORD = getenv('DB_PASSWORD')
HOST = getenv('DB_HOST')
DB = getenv('DB_DATABASE')

config = context.config
SQL_URL =  f'{PROTOCOL}+{DRIVER}://'
if USERNAME and PASSWORD: SQL_URL += f'{USERNAME}:{PASSWORD}@'

SQL_URL += f'{HOST}'

if DB: SQL_URL += f'/{DB}'

config.set_main_option('sqlalchemy.url', SQL_URL)


if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()