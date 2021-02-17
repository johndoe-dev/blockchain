from app import create_app, server


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
