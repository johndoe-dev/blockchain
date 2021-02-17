from http import HTTPStatus
import json


class TestBlockChainApi:

    def test_init_ok(self, app, data):
        test_client = app.test_client()

        resp = test_client.post(
            "/blockchain/init",
            data=json.dumps(data),
            content_type="application/json",
        )

        data = json.loads(resp.data.decode())
        assert len(data) == 1
        assert resp.status_code == HTTPStatus.CREATED
        assert data[0]["index"] == 0
        assert not data[0]["previous_hash"]
        assert data[0]["timestamp"]
        assert data[0]["data"]["mac"] == "02:02:00:9i:43"
        assert data[0]["data"]["rssi"] == "-95"
        assert data[0]["hash"]

    # def test_get_ok(self, app):
    #     test_client = app.test_client()
    #
    #     resp = test_client.get("/blockchain/init")
    #     data = json.loads(resp.data.decode())
    #     assert resp.status_code == HTTPStatus.OK
    #     assert data
