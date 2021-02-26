import os
import logging
from datetime import datetime
from flask import Flask, request
from app.custom_extensions.flask_logger import FlaskLogger


class Server:

    __app = None

    def __init__(self):
        """
        When we instantiate the Server, we also instantiate all the extensions
        """
        # instantiate extensions
        self.__instantiate_extensions()

    def __call__(self, *args, **kwargs):
        """
        Method to create the Flask app
        :param args:
        :param kwargs:
        :return:
        """
        # instantiate the app
        self.__app = Flask(__name__)

        # set config
        app_settings = os.getenv("APP_SETTINGS", "app.config.DevelopmentConfig")
        self.config.from_object(app_settings)

        # set up extensions
        self.__initialize_extensions()

        self.__app.logger.info("App started")

        from app.blockchain_api.views import block_chain_blueprint

        # register blueprints
        blueprints = {
            block_chain_blueprint: "/blockchain"
        }
        self.__register_blueprints(blueprints=blueprints)

        @self.__app.after_request
        def after_request(response):
            """ Logging after every request. """
            logger = logging.getLogger("app.access")
            logger.info(
                "%s [%s] %s %s %s %s %s %s %s",
                request.remote_addr,
                datetime.utcnow().strftime("%d/%b/%Y:%H:%M:%S.%f")[:-3],
                request.method,
                request.path,
                request.scheme,
                response.status,
                response.content_length,
                request.referrer,
                request.user_agent,
            )
            return response

        # shell context for flask cli
        @self.__app.shell_context_processor
        def ctx():
            return {"app": self.__app}

        return self.__app

    def __instantiate_extensions(self):
        """
        Method to instantiate all the extensions of Flask

        You can add the flask extensions here
        Next you will need to initialise your extensions in the method __initialize_extensions
        Example:
        self.__db = SQLAlchemy()

        :return:
        """
        self.__flask_logger = FlaskLogger()

    def __initialize_extensions(self):
        """
        Method to initialize al the extensions of Flask

        You can init your flask extensions here, don't forget to instantiate your extension
        Example:
        self.__db.init_app(self.__app)

        After initialized your extensions, you need to create a property to access your extensions
        Example:
        class Server:
            ...

            @property
            def db():
                return self.__db

        You can access the db with the server instance:
        Example:
        server = Server()
        db = server.db


        :return:
        """
        self.__flask_logger.init_app(self.__app)

    def __register_blueprints(self, **imports):
        """
        Method to register all the blueprint
        :param blueprints:
        :return:
        """
        blueprints = imports["blueprints"]

        for blueprint, url_prefix in blueprints.items():
            self.__app.register_blueprint(blueprint, url_prefix=url_prefix)

    @property
    def config(self):
        return self.__app.config


server = Server()


def create_app():
    return server()

