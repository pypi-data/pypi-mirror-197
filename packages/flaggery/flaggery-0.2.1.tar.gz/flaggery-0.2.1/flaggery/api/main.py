from importlib.metadata import metadata

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from flaggery.api.exceptions import setup_exception_handlers
from flaggery.api.routers import v1
from flaggery.api.settings import Settings

config = Settings()

meta = metadata("flaggery")

app = FastAPI(
    title=meta["name"].capitalize(),
    description=meta["summary"],
    contact={"name": "Homepage", "url": meta["home-page"]},
    license_info={"name": "License: " + meta["license"], "url": "https://spdx.org/licenses/CDDL-1.1.html"},
    version=meta["version"],
    debug=False,
)

app.include_router(v1.router)

if config.enable_prometheus:
    Instrumentator().instrument(app).expose(app)

setup_exception_handlers(app)
