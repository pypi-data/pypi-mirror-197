from fastapi import Request, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from flaggery import exceptions as exc


class NotAdmin(Exception):
    status_code = status.HTTP_423_LOCKED


def generic_handler(_: Request, e: Exception, status_code=500):

    for code_attr in ["status_code", "code"]:
        if isinstance(c := getattr(e, code_attr, None), int):
            status_code = c
            break

    for msg_attr in ["message", "description", "detail"]:
        if hasattr(e, msg_attr):
            message = getattr(e, msg_attr)
            break
    else:
        if len(e.args) > 0:
            message = e.args[0]
        else:
            message = str(e)

    return JSONResponse(
        status_code=status_code,
        content={"exception": {"name": e.__class__.__name__, "message": message}},
    )


def generic_handler_with_code(status_code: int):
    def handler(_: Request, e: Exception):
        return generic_handler(_, e, status_code)

    return handler


def setup_exception_handlers(app: FastAPI):
    for exc_class in [Exception, HTTPException]:
        app.exception_handler(exc_class)(generic_handler)

    for code, exc_classes in {
        status.HTTP_404_NOT_FOUND: {exc.SubjectNotFound, exc.FeatureNotFound, exc.VariantNotFound,
                                    exc.GroupNotFound, exc.AbTestNotFound, exc.RolloutNotFound,
                                    exc.BucketNotFound},
        status.HTTP_400_BAD_REQUEST: {exc.VariantExists, exc.AbTestExists, exc.GroupExists,
                                      exc.SubjectExists, exc.FeatureExists, exc.RolloutExists,
                                      exc.ValidationError, exc.InvalidRolloutProportion, exc.SubjectAlreadyInGroup},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {exc.NoBuckets, exc.FailedToAddBucket, exc.FailedToLoadPlugin}
    }.items():
        for exc_class in exc_classes:
            app.exception_handler(exc_class)(generic_handler_with_code(code))
