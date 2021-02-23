import json
import copy
from http import HTTPStatus


class TestBlockChainInitApi:

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

    def test_init_block_chain_add_block_when_already_init(self, app, data):
        test_client = app.test_client()

        test_client.post(
            "/blockchain/init",
            data=json.dumps(data),
            content_type="application/json",
        )

        resp = test_client.post(
            "/blockchain/init",
            data=json.dumps(data),
            content_type="application/json",
        )

        assert resp.status_code == HTTPStatus.CREATED

        data = json.loads(resp.data.decode())
        assert len(data) == 2
        assert data[0]["index"] == 0
        assert not data[0]["previous_hash"]
        assert data[0]["timestamp"]
        assert data[0]["data"]["mac"] == "02:02:00:9i:43"
        assert data[0]["data"]["rssi"] == "-95"
        assert data[0]["hash"]

        assert data[1]["index"] == 1
        assert data[1]["previous_hash"] == data[0]["hash"]
        assert data[1]["timestamp"]
        assert data[1]["data"]["mac"] == "02:02:00:9i:43"
        assert data[1]["data"]["rssi"] == "-95"
        assert data[1]["hash"]

    def test_init_failed_when_data_invalid(self, app):
        test_client = app.test_client()

        resp = test_client.post(
            "/blockchain/init",
            data=json.dumps({}),
            content_type="application/json",
        )

        assert resp.status_code == HTTPStatus.BAD_REQUEST

        data = json.loads(resp.data.decode())
        assert data == "Invalid data received to create a block"

    def test_init_block_chain_from_list(self, app, block_chain_json, expected_block_chain_json):
        with open(block_chain_json, "r") as block_chain_json_file:
            block_chain_data = json.load(block_chain_json_file)

        test_client = app.test_client()

        resp = test_client.post(
            "/blockchain/init?from_json",
            data=json.dumps(block_chain_data),
            content_type="application/json",
        )

        assert resp.status_code == HTTPStatus.CREATED

        data = json.loads(resp.data.decode())
        assert len(data) == 4
        assert data == expected_block_chain_json

    def test_init_block_chain_from_list_failed_when_missing_key(self, app, block_chain_json):
        with open(block_chain_json, "r") as block_chain_json_file:
            block_chain_data = json.load(block_chain_json_file)

        del block_chain_data[0]["index"]

        test_client = app.test_client()

        resp = test_client.post(
            "/blockchain/init?from_json",
            data=json.dumps(block_chain_data),
            content_type="application/json",
        )

        assert resp.status_code == HTTPStatus.BAD_REQUEST

    def test_init_block_chain_from_list_failed_when_block_chain_is_not_valid(self, app, block_chain_json):
        with open(block_chain_json, "r") as block_chain_json_file:
            block_chain_data = json.load(block_chain_json_file)

        block_chain_data[1]["hash"] = "invalid hash"

        test_client = app.test_client()

        resp = test_client.post(
            "/blockchain/init?from_json",
            data=json.dumps(block_chain_data),
            content_type="application/json",
        )

        assert resp.status_code == HTTPStatus.BAD_REQUEST


class TestBlockChainApi:

    def test_add_block_ok(self, app, data):
        test_client = app.test_client()

        test_client.post(
            "/blockchain/init",
            data=json.dumps(data),
            content_type="application/json",
        )

        resp = test_client.post(
            "blockchain/add",
            data=json.dumps(data),
            content_type="application/json",
        )

        data = json.loads(resp.data.decode())

        assert len(data) == 2
        assert resp.status_code == HTTPStatus.CREATED

        assert data[0]["index"] == 0
        assert not data[0]["previous_hash"]
        assert data[0]["timestamp"]
        assert data[0]["data"]["mac"] == "02:02:00:9i:43"
        assert data[0]["data"]["rssi"] == "-95"
        assert data[0]["hash"]

        assert data[1]["index"] == 1
        assert data[1]["previous_hash"] == data[0]["hash"]
        assert data[1]["timestamp"]
        assert data[1]["data"]["mac"] == "02:02:00:9i:43"
        assert data[1]["data"]["rssi"] == "-95"
        assert data[1]["hash"]

    def test_add_block_failed_when_block_chain_not_initialized(self, app, data):
        test_client = app.test_client()

        resp = test_client.post(
            "blockchain/add",
            data=json.dumps(data),
            content_type="application/json",
        )

        assert resp.status_code == HTTPStatus.BAD_REQUEST

        data = json.loads(resp.data.decode())
        assert data == "BlockChain has not been initialized"

    def test_add_block_failed_when_data_invalid(self, app, data):
        test_client = app.test_client()

        test_client.post(
            "/blockchain/init",
            data=json.dumps(data),
            content_type="application/json",
        )

        resp = test_client.post(
            "blockchain/add",
            data=json.dumps({}),
            content_type="application/json",
        )

        assert resp.status_code == HTTPStatus.BAD_REQUEST

        data = json.loads(resp.data.decode())
        assert data == "Invalid data received to create a block"


class TestBlockChainCompareApi:

    def test_compare_block_chain_ok(self, app, block_chain_json, expected_block_chain_json):
        test_client = app.test_client()

        with open(block_chain_json, "r") as block_chain_json_file:
            first_block_chain = json.load(block_chain_json_file)

        second_block_chain = copy.deepcopy(first_block_chain)

        second_block_chain[3]["data"] = "different data"

        resp = test_client.post(
            "blockchain/compare",
            data=json.dumps({
                "first_block_chain": first_block_chain,
                "second_block_chain": second_block_chain
            }),
            content_type="application/json",
        )

        assert resp.status_code == HTTPStatus.CREATED

        data = json.loads(resp.data.decode())

        assert len(data) == 5
        assert data[:-1] == expected_block_chain_json
        assert data[-1]["index"] == 4
        assert data[-1]["previous_hash"] == expected_block_chain_json[-1]["hash"]
        assert data[-1]["timestamp"]
        assert data[-1]["data"] == "different data"
        assert data[-1]["hash"]

    def test_compare_block_chain_failed_when_bad_key_for_block_chain(self, app, block_chain_json):
        test_client = app.test_client()

        with open(block_chain_json, "r") as block_chain_json_file:
            first_block_chain = json.load(block_chain_json_file)

        second_block_chain = copy.deepcopy(first_block_chain)

        resp = test_client.post(
            "blockchain/compare",
            data=json.dumps({
                "first_block_chain": first_block_chain,
                "bad_key": second_block_chain
            }),
            content_type="application/json",
        )

        assert resp.status_code == HTTPStatus.BAD_REQUEST

        data = json.loads(resp.data.decode())

        assert data == "Data miss keys : 'second_block_chain'"

    def test_compare_block_chain_failed_when_missing_key(self, app, block_chain_json):
        test_client = app.test_client()

        with open(block_chain_json, "r") as block_chain_json_file:
            first_block_chain = json.load(block_chain_json_file)

        second_block_chain = copy.deepcopy(first_block_chain)

        del first_block_chain[0]["index"]

        resp = test_client.post(
            "blockchain/compare",
            data=json.dumps({
                "first_block_chain": first_block_chain,
                "second_block_chain": second_block_chain
            }),
            content_type="application/json",
        )

        assert resp.status_code == HTTPStatus.BAD_REQUEST

        data = json.loads(resp.data.decode())

        assert data == "Invalid list to create blockchain"

    def test_compare_block_chain_failed_when_block_chain_is_not_valid(self, app, block_chain_json):
        test_client = app.test_client()

        with open(block_chain_json, "r") as block_chain_json_file:
            first_block_chain = json.load(block_chain_json_file)

        second_block_chain = copy.deepcopy(first_block_chain)

        first_block_chain[1]["hash"] = "invalid hash"

        resp = test_client.post(
            "blockchain/compare",
            data=json.dumps({
                "first_block_chain": first_block_chain,
                "second_block_chain": second_block_chain
            }),
            content_type="application/json",
        )

        assert resp.status_code == HTTPStatus.BAD_REQUEST

        data = json.loads(resp.data.decode())

        assert data == "Blockchain  invalid"
