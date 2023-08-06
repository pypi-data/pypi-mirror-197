from fastapi import APIRouter
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
