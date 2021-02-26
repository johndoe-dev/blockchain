def fixture_logger_handler_watched(logger):
    return {
        "handlers": {
            "default": {
                "level": logger.logging_level,
                "class": logger.logging_policy,
                "filename": logger.app_log,
                "formatter": "default",
                "delay": True,
            },
            "access_logs": {
                "level": logger.logging_level,
                "class": logger.logging_policy,
                "filename": logger.www_log,
                "formatter": "access",
                "delay": True,
            }
        }
    }


def fixture_logger_handler_stream(logger):
    return {
        "handlers": {
            "default": {
                "level": logger.logging_level,
                "formatter": "default",
                "class": logger.logging_policy,
            },
            "access_logs": {
                "level": logger.logging_level,
                "class": logger.logging_policy,
                "formatter": "access",
            },
        }
    }


def fixture_logger_handler_rotating(logger):
    return {
        "handlers": {
            "default": {
                "level": logger.logging_level,
                "class": logger.logging_policy,
                "filename": logger.app_log,
                "backupCount": logger.log_copies,
                "maxBytes": logger.log_max_bytes,
                "formatter": "default",
                "delay": True,
            },
            "access_logs": {
                "level": logger.logging_level,
                "class": logger.logging_policy,
                "filename": logger.www_log,
                "backupCount": logger.log_copies,
                "maxBytes": logger.log_max_bytes,
                "formatter": "access",
                "delay": True,
            },
        }
    }
