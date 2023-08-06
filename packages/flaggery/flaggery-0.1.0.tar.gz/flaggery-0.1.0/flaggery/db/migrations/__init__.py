import os

from alembic import command
from alembic.config import Config
from sqlalchemy import Engine


def get_alembic_config(db_url):
    alembic_dir = os.path.dirname(os.path.abspath(__file__))
    # Escape any '%' that appears in a db_url. This could be in a password,
    # url, or anything that is part of a potentially complex database url
    db_url = db_url.replace("%", "%%")
    config = Config(os.path.join(alembic_dir, "alembic.ini"))
    config.set_main_option("script_location", alembic_dir)
    config.set_main_option("sqlalchemy.url", db_url)
    return config


def upgrade_db(engine: Engine, version: str = 'head'):
    db_url = str(engine.url)
    config = get_alembic_config(db_url)
    with engine.begin() as connection:
        config.attributes["connection"] = connection
        command.upgrade(config, version)
