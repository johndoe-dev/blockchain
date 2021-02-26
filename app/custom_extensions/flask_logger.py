import os
from pathlib import Path
from logging.config import dictConfig
from flask import Flask


class FlaskLogger:

    def __init__(self, app=None, **kwargs):
        self.log_type = None
        self.logging_level = None
        self.log_directory = None
        self.app_log_file_name = None
        self.access_log_file_name = None
        self.app_log = None
        self.www_log = None
        self.logging_handler = {}
        self.logging_policy = None

        self.log_max_bytes = None
        self.log_copies = None

        self.std_format = {}
        self.std_logger = {}

        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app: Flask, **kwargs):
        self.log_type = app.config.get("LOG_TYPE", "stream")
        self.logging_level = app.config.get("LOG_LEVEL", "INFO")

        log_type_accepted = ["stream", "watched", "rotating"]

        self.std_format = {
            "formatters": {
                "default": {
                    "format": "[%(asctime)s.%(msecs)03d] %(levelname)s %(name)s:%(funcName)s: %(message)s",
                    "datefmt": "%d/%b/%Y:%H:%M:%S",
                },
                "access": {"format": "%(message)s"},
            }
        }
        self.std_logger = {
            "loggers": {
                "": {"level": self.logging_level, "handlers": ["default"], "propagate": True},
                "app.access": {
                    "level": self.logging_level,
                    "handlers": ["access_logs"],
                    "propagate": False,
                },
                "root": {"level": self.logging_level, "handlers": ["default"]},
            }
        }

        if self.log_type not in log_type_accepted:
            exit(code=f"log_type must be in '{', '.join(log_type_accepted)}' but was '{self.log_type}'")

        if self.log_type == "stream":
            self.get_stream_handler()

        if self.log_type == "watched":
            self.check_config_for_handler(app)
            self.get_watched_file_handler()

        if self.log_type == "rotating":
            self.check_config_for_handler(app)
            self.log_max_bytes = app.config["LOG_MAX_BYTES"]
            self.log_copies = app.config["LOG_COPIES"]
            self.get_rotating_file_handler()

        self.log_config()

    def get_stream_handler(self):
        self.logging_policy = "logging.StreamHandler"

        self.logging_handler = {
            "handlers": {
                "default": {
                    "level": self.logging_level,
                    "formatter": "default",
                    "class": self.logging_policy,
                },
                "access_logs": {
                    "level": self.logging_level,
                    "class": self.logging_policy,
                    "formatter": "access",
                },
            }
        }

    def get_watched_file_handler(self):
        self.logging_policy = "logging.handlers.WatchedFileHandler"

        self.logging_handler = {
            "handlers": {
                "default": {
                    "level": self.logging_level,
                    "class": self.logging_policy,
                    "filename": self.app_log,
                    "formatter": "default",
                    "delay": True,
                },
                "access_logs": {
                    "level": self.logging_level,
                    "class": self.logging_policy,
                    "filename": self.www_log,
                    "formatter": "access",
                    "delay": True,
                },
            }
        }

    def get_rotating_file_handler(self):
        self.logging_policy = "logging.handlers.RotatingFileHandler"

        self.logging_handler = {
            "handlers": {
                "default": {
                    "level": self.logging_level,
                    "class": self.logging_policy,
                    "filename": self.app_log,
                    "backupCount": self.log_copies,
                    "maxBytes": self.log_max_bytes,
                    "formatter": "default",
                    "delay": True,
                },
                "access_logs": {
                    "level": self.logging_level,
                    "class": self.logging_policy,
                    "filename": self.www_log,
                    "backupCount": self.log_copies,
                    "maxBytes": self.log_max_bytes,
                    "formatter": "access",
                    "delay": True,
                },
            }
        }

    def check_config_for_handler(self, app):
        base_dir = Path(__file__).parents[2]

        try:
            self.log_directory = base_dir / app.config["LOG_DIR"].replace("/", "")
            self.app_log_file_name = app.config["APP_LOG_NAME"].replace("/", "")
            self.access_log_file_name = app.config["WWW_LOG_NAME"].replace("/", "")
        except KeyError as e:
            exit(code=f"{e} is a required parameter for log_type '{self.log_type}'")

        self.app_log = self.log_directory / self.app_log_file_name
        self.www_log = self.log_directory / self.access_log_file_name

        if not os.path.isdir(self.log_directory):
            os.mkdir(self.log_directory)

    def log_config(self):
        log_config = {
            "version": 1,
            "formatters": self.std_format["formatters"],
            "loggers": self.std_logger["loggers"],
            "handlers": self.logging_handler["handlers"],
        }
        dictConfig(log_config)
