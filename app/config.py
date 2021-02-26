import os


class BaseConfig:
    """Base configuration"""

    PROD = False

    LOG_TYPE = os.environ.get("LOG_TYPE", "watched")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

    # File Logging Setup
    LOG_DIR = os.environ.get("LOG_DIR", "/logs")
    APP_LOG_NAME = os.environ.get("APP_LOG_NAME", "app.log")
    WWW_LOG_NAME = os.environ.get("WWW_LOG_NAME", "www.log")
    LOG_MAX_BYTES = os.environ.get("LOG_MAX_BYTES", 100_000_000)  # 100MB in bytes
    LOG_COPIES = os.environ.get("LOG_COPIES", 5)


class DevelopmentConfig(BaseConfig):
    """Development configuration"""


class TestingConfig(BaseConfig):
    """Testing configuration"""

    TESTING = True
    LOG_DIR = os.environ.get("LOG_DIR", "/test_logs")


class ProductionConfig(BaseConfig):
    """Production configuration"""

    PROD = True
