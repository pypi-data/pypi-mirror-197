from typing import Union

from fastapi import Request, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import ProgrammingError, OperationalError

from flaggery import exceptions as exc


class NotAdmin(Exception):
    pass


def format_exc(exception: Exception):
    for msg_attr in ["message", "description", "detail"]:
        if hasattr(exception, msg_attr):
            message = getattr(exception, msg_attr)
            break
    else:
        message = " | ".join((str(arg) for arg in exception.args))
    return {"name": exception.__class__.__name__, "message": message}


def generic_handler(_: Request, exception: Exception, status_code=500):
    content = {"exception": format_exc(exception)}

    if cause := getattr(exception, "cause", None):
        content["cause"] = format_exc(cause)

    return JSONResponse(status_code=status_code, content=content)


def generic_handler_with_code(status_code: int):
    def handler(_: Request, exception: Exception):
        return generic_handler(_, exception, status_code)

    return handler


def handle_db_errors(_: Request, exception: Union[ProgrammingError, OperationalError]):
    content = {
        "exception": {
            "name": exception.__class__.__name__,
            "message": "",
            "cause": {
                "name": exception._message().split(")")[0].lstrip("("),
                "message": exception._message().split(")")[1].lstrip(" "),
            },
        }
    }

    return JSONResponse(status_code=500, content=content)


def setup_exception_handlers(app: FastAPI):
    for exc_class in [Exception, HTTPException]:
        app.exception_handler(exc_class)(generic_handler)

    for exc_class in [ProgrammingError, OperationalError]:
        app.exception_handler(exc_class)(handle_db_errors)

    for code, exc_classes in {
        status.HTTP_404_NOT_FOUND: {
            exc.SubjectNotFound,
            exc.FeatureNotFound,
            exc.VariantNotFound,
            exc.GroupNotFound,
            exc.AbTestNotFound,
            exc.RolloutNotFound,
            exc.BucketNotFound,
        },
        status.HTTP_400_BAD_REQUEST: {
            exc.VariantExists,
            exc.AbTestExists,
            exc.GroupExists,
            exc.SubjectExists,
            exc.FeatureExists,
            exc.RolloutExists,
            exc.ValidationError,
            exc.InvalidRolloutProportion,
            exc.SubjectAlreadyInGroup,
            exc.SubjectNotInGroup,
            exc.FeatureHasChildren,
            exc.VariantIsUsed,
        },
        status.HTTP_423_LOCKED: {
            NotAdmin,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {exc.NoBuckets, exc.FailedToAddBucket, exc.FailedToLoadPlugin},
    }.items():
        for exc_class in exc_classes:
            app.exception_handler(exc_class)(generic_handler_with_code(code))
