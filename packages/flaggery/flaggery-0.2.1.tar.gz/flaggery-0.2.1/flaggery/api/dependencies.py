from flaggery.api.settings import Settings
from flaggery.core import Flaggery

config = Settings()

flaggery = Flaggery.from_db_url(config.db_url)

if config.db_auto_upgrade:
    flaggery.upgrade_db()


def get_flaggery() -> Flaggery:
    yield flaggery
