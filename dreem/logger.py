import os
import logging
import colorlog

APP_LOGGER_NAME = "dreem"


class DreemError(Exception):
    pass


log_format = (
    "[%(asctime)s " "%(name)s " "%(funcName)s] " "%(levelname)s " "%(message)s"
)


def get_stream_handler():
    colorlog_format = f"%(log_color)s" f"{log_format}"
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            colorlog_format,
            datefmt="%H:%M",
            reset=True,
            log_colors={
                "DEBUG": "cyan",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
    )
    return handler


def get_file_handler(log_outfile):
    fileHandler = logging.FileHandler(log_outfile, mode="w")
    fileHandler.setFormatter(logging.Formatter(log_format))
    return fileHandler


def setup_applevel_logger(
    logger_name=APP_LOGGER_NAME,
    log_outfile=None,
    is_debug=False
) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG if is_debug else logging.INFO)
    logger.addHandler(get_stream_handler())
    if log_outfile is not None:
        logger.addHandler(get_file_handler(log_outfile))
    return logger


def get_logger(module_name):
    return logging.getLogger(APP_LOGGER_NAME).getChild(module_name)


def log_error_and_exit(log, msg):
    log.error(msg)
    raise DreemError(msg)


def str_to_log_level(s: str):
    s = s.rstrip().lstrip().lower()
    if s == "info":
        return logging.INFO
    elif s == "debug":
        return logging.DEBUG
    elif s == "warn":
        return logging.WARN
    elif s == "error":
        return logging.ERROR
    elif s == "critical":
        return logging.CRITICAL
    else:
        raise ValueError("unknown log level: {}".format(s))
