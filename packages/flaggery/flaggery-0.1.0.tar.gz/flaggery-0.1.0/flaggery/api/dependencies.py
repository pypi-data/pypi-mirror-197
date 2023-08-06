from sqlalchemy import create_engine

from flaggery.api.settings import Settings
from flaggery.core import Flaggery
from flaggery.db.migrations import upgrade_db

config = Settings()

engine = create_engine(config.db_url)

flaggery = Flaggery(engine)

if config.db_auto_upgrade:
    upgrade_db(engine)


def get_flaggery() -> Flaggery:
    yield flaggery
