import pytest
from pathlib import Path
from tests.base_test import BaseFlaskTest
from app.custom_extensions.flask_logger import FlaskLogger


def concatenate_path(*paths):
    base_dir = Path(__file__).parents[2]
    for path in paths:
        base_dir /= path

    return base_dir


class TestFlaskLogger(BaseFlaskTest):
    def test_init_flask_logger_with_watched_ok(self, config, logger_handler_watched):
        self.app.config.from_object(config["test"])

        self.app.config["LOG_TYPE"] = "watched"

        logger = FlaskLogger(self.app)

        assert logger.log_directory == self.concatenate_path("test_logs")
        assert logger.logging_handler == logger_handler_watched(logger)

    def test_init_flask_logger_with_stream_ok(self, config, logger_handler_stream):
        self.app.config.from_object(config["test"])

        self.app.config["LOG_TYPE"] = "stream"

        logger = FlaskLogger(self.app)

        assert logger.logging_handler == logger_handler_stream(logger)

    def test_init_flask_logger_with_rotating_ok(self, config, logger_handler_rotating):
        self.app.config.from_object(config["test"])

        self.app.config["LOG_TYPE"] = "rotating"

        logger = FlaskLogger(self.app)

        assert logger.log_directory == self.concatenate_path("test_logs")
        assert logger.logging_handler == logger_handler_rotating(logger)

    def test_init_flask_logger_failed_when_bad_log_type(self, config):
        self.app.config.from_object(config["test"])

        self.app.config["LOG_TYPE"] = "bad_type"

        with pytest.raises(SystemExit) as e:
            FlaskLogger(self.app)

        assert e.value.code == "log_type must be in 'stream, watched, rotating' but was 'bad_type'"

    def test_init_flask_logger_failed_when_missing_config(self, config):
        self.app.config.from_object(config["test"])

        self.app.config["LOG_TYPE"] = "watched"

        del self.app.config["LOG_DIR"]

        with pytest.raises(SystemExit) as e:
            FlaskLogger(self.app)

        assert e.value.code == "'LOG_DIR' is a required parameter for log_type 'watched'"

