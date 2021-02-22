import json
import pytest
from tests.base_test import Base
from app.models import BlockChainDataInvalid, BlockChainNotInitializedError, BlockChainInvalid, BlockChainInvalidList
from app.blockchain_api.controllers import blockchain_controller


class TestBlockChainController(Base):

    def test_init_block_chain(self, data):
        result = blockchain_controller.init_block_chain(self.block_chain, data)
        assert len(result) == 1
        assert result[0]["index"] == 0
        assert not result[0]["previous_hash"]
        assert result[0]["timestamp"]
        assert result[0]["data"]["mac"] == "02:02:00:9i:43"
        assert result[0]["data"]["rssi"] == "-95"
        assert result[0]["hash"]

    def test_init_block_chain_add_block_when_already_init(self, data):
        self.block_chain.init_first(data)

        # with pytest.raises(BlockChainAlreadyInitError):
        result = blockchain_controller.init_block_chain(self.block_chain, data)

        assert len(result) == 2
        assert result[0]["index"] == 0
        assert not result[0]["previous_hash"]
        assert result[0]["timestamp"]
        assert result[0]["data"]["mac"] == "02:02:00:9i:43"
        assert result[0]["data"]["rssi"] == "-95"
        assert result[0]["hash"]

        assert result[1]["index"] == 1
        assert result[1]["previous_hash"] == result[0]["hash"]
        assert result[1]["timestamp"]
        assert result[1]["data"]["mac"] == "02:02:00:9i:43"
        assert result[1]["data"]["rssi"] == "-95"
        assert result[1]["hash"]

    def test_init_block_chain_failed_when_data_invalid(self):
        with pytest.raises(BlockChainDataInvalid):
            blockchain_controller.init_block_chain(self.block_chain, {})

    def test_add_block(self, data):
        blockchain_controller.init_block_chain(self.block_chain, data)

        result = blockchain_controller.add_block(self.block_chain, data)

        assert len(result) == 2
        assert result[0]["index"] == 0
        assert not result[0]["previous_hash"]
        assert result[0]["timestamp"]
        assert result[0]["data"]["mac"] == "02:02:00:9i:43"
        assert result[0]["data"]["rssi"] == "-95"
        assert result[0]["hash"]

        assert result[1]["index"] == 1
        assert result[1]["previous_hash"] == result[0]["hash"]
        assert result[1]["timestamp"]
        assert result[1]["data"]["mac"] == "02:02:00:9i:43"
        assert result[1]["data"]["rssi"] == "-95"
        assert result[1]["hash"]

    def test_add_block_failed_when_not_initialized(self, data):
        with pytest.raises(BlockChainNotInitializedError):
            blockchain_controller.add_block(self.block_chain, data)

    def test_add_block_failed_when_data_invalid(self, data):
        blockchain_controller.init_block_chain(self.block_chain, data)

        with pytest.raises(BlockChainDataInvalid):
            blockchain_controller.add_block(self.block_chain, {})

    def test_init_block_chain_from_list(self, block_chain_json, expected_block_chain_json):
        with open(block_chain_json, "r") as block_chain_json_file:
            block_chain_data = json.load(block_chain_json_file)

        result = blockchain_controller.init_block_chain_from_list(self.block_chain, block_chain_data)

        assert len(result) == 4
        assert result == expected_block_chain_json

    def test_init_block_chain_from_list_failed_when_missing_key(self, block_chain_json):
        with open(block_chain_json, "r") as block_chain_json_file:
            block_chain_data = json.load(block_chain_json_file)

        del block_chain_data[0]["index"]

        with pytest.raises(BlockChainInvalidList):
            blockchain_controller.init_block_chain_from_list(self.block_chain, block_chain_data)

    def test_init_block_chain_from_list_failed_when_block_chain_is_not_valid(self, block_chain_json):
        with open(block_chain_json, "r") as block_chain_json_file:
            block_chain_data = json.load(block_chain_json_file)

        block_chain_data[1]["hash"] = "invalid hash"

        with pytest.raises(BlockChainInvalid):
            blockchain_controller.init_block_chain_from_list(self.block_chain, block_chain_data)
