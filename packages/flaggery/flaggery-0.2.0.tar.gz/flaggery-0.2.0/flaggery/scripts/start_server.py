import argparse
import logging
import multiprocessing
import sys

from loguru import logger

from flaggery.api.common import StandaloneApplication, StubbedGunicornLogger, InterceptHandler


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="The network address to listen on (default: 127.0.0.1). "
        "Use 0.0.0.0 to bind to all addresses if you want to access the server from other machines.",
    )
    parser.add_argument("--port", type=int, default=8080, help="The port to listen on (default: 8080)")
    parser.add_argument(
        "--workers",
        type=int,
        default=multiprocessing.cpu_count(),
        help="Number of worker processes to handle requests (default: cpu count)",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["critical", "error", "warning", "info", "debug", "trace"],
        default="info",
        help="Log level (default: info)",
    )
    parser.add_argument("--json-logs", action="store_true", help="(Boolean flag) Serialize logs in json format")
    return parser


def setup_logging(log_level: str, json_logs: bool):
    intercept_handler = InterceptHandler()
    logging.root.setLevel(log_level.upper())

    for name in {
        *logging.root.manager.loggerDict.keys(),  # pylint: disable=E1101
        "gunicorn",
        "gunicorn.access",
        "gunicorn.error",
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
    }:
        logging.getLogger(name).handlers = [intercept_handler]

    logger.configure(handlers=[{"sink": sys.stdout, "serialize": json_logs, "level": log_level.upper()}])


def main():
    args = get_parser().parse_args()

    from flaggery.api.main import app  # pylint: disable=C0415

    setup_logging(args.log_level, args.json_logs)

    options = {
        "bind": f"{args.host}:{args.port}",
        "workers": args.workers,
        "log_level": args.log_level,
        "accesslog": "-",
        "errorlog": "-",
        "worker_class": "uvicorn.workers.UvicornWorker",
        "logger_class": StubbedGunicornLogger,
    }

    StandaloneApplication(app, options).run()


if __name__ == "__main__":
    main()
