from flask import Flask

from app.models import Block, BlockChain, BlockChainException


__all__ = ("Block", "BlockChain", "BlockChainException", "server", "create_app")


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

        # set up extensions
        self.__initialize_extensions()

        from app.blockchain_api.views import block_chain_blueprint

        # register blueprints
        blueprints = {
            block_chain_blueprint: "/blockchain"
        }
        self.__register_blueprints(blueprints=blueprints)

        # shell context for flask cli
        @self.__app.shell_context_processor
        def ctx():
            return {"app": self.__app}

        return self.__app

    def __instantiate_extensions(self):
        """
        Method to instantiate all the extensions of Flask
        :return:
        """

    def __initialize_extensions(self):
        """
        Method to initialize al the extensions of Flask
        :return:
        """

    def __register_blueprints(self, **imports):
        """
        Method to register all the blueprint
        :param blueprints:
        :return:
        """
        blueprints = imports["blueprints"]

        for blueprint, url_prefix in blueprints.items():
            self.__app.register_blueprint(blueprint, url_prefix=url_prefix)


server = Server()


def create_app():
    return server()

