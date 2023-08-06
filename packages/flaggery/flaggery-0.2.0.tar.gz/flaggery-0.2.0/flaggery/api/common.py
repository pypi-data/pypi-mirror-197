import logging

from fastapi import APIRouter
from gunicorn.app.base import BaseApplication
from gunicorn.glogging import Logger
from loguru import logger
from merge_args import merge_args
from starlette.routing import Route

from flaggery.api.exceptions import NotAdmin
from flaggery.api.settings import Settings

config = Settings()


def admin_route(router: APIRouter):
    def handle_not_admin(*_, **__):
        raise NotAdmin("Request unacceptable. Server is not on admin mode.")

    def decorator(_):
        if not config.admin_mode:
            original: Route = router.routes[-1]
            original.endpoint = merge_args(original.endpoint)(handle_not_admin)

    return decorator


class StandaloneApplication(BaseApplication):
    def init(self, parser, opts, args):
        pass

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        cfg = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
        for key, value in cfg.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


class StubbedGunicornLogger(Logger):
    def setup(self, cfg):
        handler = logging.NullHandler()
        self.error_logger = logging.getLogger("gunicorn.error")
        self.error_logger.addHandler(handler)
        self.access_logger = logging.getLogger("gunicorn.access")
        self.access_logger.addHandler(handler)
        self.error_logger.setLevel(cfg.loglevel.upper())
        self.access_logger.setLevel(cfg.loglevel.upper())


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
