import shutil
from pathlib import Path
from flask import Flask
from app import create_app, server
from app.models import BlockChain


class BaseTest:
    app = None
    client_app = None

    @classmethod
    def setup_class(cls):
        app = create_app()
        app.testing = True

        cls.server = server
        cls.app = app
        cls.ctx = app.app_context()
        cls.ctx.push()
        cls.client_app = app.test_client()

    @classmethod
    def teardown_class(cls):
        cls.ctx.pop()


class BaseFlaskTest:
    app = None
    path = None

    @classmethod
    def setup_class(cls):
        app = Flask(__name__)
        app.testing = True

        cls.app = app
        cls.ctx = app.app_context()
        cls.ctx.push()

    @classmethod
    def concatenate_path(cls, *paths):
        base_dir = Path(__file__).parents[1]
        for path in paths:
            base_dir /= path

        cls.path = base_dir
        return base_dir

    @classmethod
    def teardown_class(cls):
        cls.ctx.pop()
        shutil.rmtree(cls.path)



class Base:
    def setup_method(self):
        self.block_chain = BlockChain()

    def teardown_method(self):
        BlockChain.blocks = []
