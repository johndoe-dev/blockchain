from tests.base_test import BaseTest


class TestServer(BaseTest):
    def test_context(self):
        ctx = self.app.shell_context_processors[0]()
        assert len(ctx) == 1
        assert "app" in ctx
