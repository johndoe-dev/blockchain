import json
import pytest
from datetime import datetime

from app.models import (
    Block,
    BlockChain,
    BlockChainAlreadyInitError,
    BlockChainNotInitializedError,
    BlockChainDataInvalid,
    BlockChainInvalid,
    BlockChainInvalidList)

from tests.base_test import Base


class TestBlock:

    def test_create_block(self, block_data):
        new_block = Block(0, None, datetime.now(), block_data[0])

        assert new_block.index == 0
        assert not new_block.previous_hash
        assert isinstance(new_block.hash, str)
        assert new_block.data

    def test_serialize(self, expected_serialized_block, block_data):
        new_block = Block(0, None, datetime.now(), block_data[0])

        assert new_block.serialize() == expected_serialized_block(new_block)


class TestBlockChain(Base):
    def test_create_block_chain_with_first_block_ok(self, block_data):
        new_block_chain = BlockChain(block_data[0])
        assert len(new_block_chain.blocks) == 1
        assert new_block_chain.is_block_chain_valid()

        first_block = new_block_chain.blocks[0]

        assert first_block.index == 0
        assert not first_block.previous_hash
        assert isinstance(first_block.hash, str)
        assert first_block.data == block_data[0]

    def test_init_first_ok(self, block_data):
        new_block_chain = BlockChain()
        new_block_chain.init_first(block_data[0])

        assert len(new_block_chain.blocks) == 1

        first_block = new_block_chain.blocks[0]

        assert first_block.index == 0
        assert not first_block.previous_hash
        assert isinstance(first_block.hash, str)
        assert first_block.data == block_data[0]

    def test_init_first_failed_when_data_invalid(self):
        new_block_chain = BlockChain()

        with pytest.raises(BlockChainDataInvalid) as e:
            new_block_chain.init_first(None)

        assert e.value.code == "invalid-data"
        assert e.value.message == "Invalid data received to create a block"

    def test_init_first_fail_when_first_block_already_exist(self, block_data):
        new_block_chain = BlockChain(block_data[0])

        with pytest.raises(BlockChainAlreadyInitError) as e:
            new_block_chain.init_first("first block")

        assert e.value.code == "already-initialized"
        assert e.value.message == "BlockChain already initialized"

    def test_create_block_chain_with_several_blocks_ok(self, block_data):
        new_block_chain = BlockChain(block_data[0])

        new_block_chain.add_block(new_block_chain.new_block(block_data[1]))
        new_block_chain.add_block(new_block_chain.new_block(block_data[2]))
        new_block_chain.add_block(new_block_chain.new_block(block_data[3]))

        expected_data = ["first block", "second block", "third block", "fourth block"]

        assert len(new_block_chain.blocks) == 4
        assert new_block_chain.is_block_chain_valid()

        for index, block in enumerate(new_block_chain.blocks):
            if index == 0:
                assert block.index == index
                assert not block.previous_hash
                assert isinstance(block.hash, str)
                assert block.data == expected_data[index]
            else:
                assert block.index == index
                assert block.previous_hash == new_block_chain.blocks[index - 1].hash
                assert isinstance(block.hash, str)
                assert block.data == expected_data[index]

    def test_add_block_chain_failed_when_data_invalid(self, block_data):
        new_block_chain = BlockChain(block_data[0])

        with pytest.raises(BlockChainDataInvalid) as e:
            new_block_chain.add_block(new_block_chain.new_block(None))

        assert e.value.code == "invalid-data"
        assert e.value.message == "Invalid data received to create a block"

    def test_create_block_chain_with_first_block_invalid_index(self, block_data):
        new_block_chain = BlockChain(block_data[0])

        bad_first_block = Block(10, None, datetime.now(), block_data[0])

        new_block_chain.blocks[0] = bad_first_block

        assert not new_block_chain.is_block_chain_valid()

    def test_create_block_chain_with_first_block_invalid_previous_hash(self, block_data):
        new_block_chain = BlockChain(block_data[0])

        bad_first_block = Block(0, "0OIJKjkghjbgghu", datetime.now(), block_data[0])

        new_block_chain.blocks[0] = bad_first_block

        assert not new_block_chain.is_block_chain_valid()

    def test_create_block_chain_with_first_block_invalid_hash(self, block_data):
        new_block_chain = BlockChain(block_data[0])

        bad_first_block = Block(0, None, datetime.now(), block_data[0])
        bad_first_block.hash = "1234"

        new_block_chain.blocks[0] = bad_first_block

        assert not new_block_chain.is_block_chain_valid()

    def test_create_block_chain_with_invalid_next_block_index(self, block_data):
        new_block_chain = BlockChain(block_data[0])

        second_block = Block(2, new_block_chain.blocks[0].hash, datetime.now(), block_data[1])
        new_block_chain.add_block(second_block)

        assert not new_block_chain.is_block_chain_valid()

    def test_create_block_chain_with_invalid_next_block_previous_hash(self, block_data):
        new_block_chain = BlockChain(block_data[0])

        second_block = Block(1, "bad previous hash", datetime.now(), block_data[1])
        new_block_chain.add_block(second_block)

        assert not new_block_chain.is_block_chain_valid()

    def test_create_block_chain_with_next_block_hash_null(self, block_data):
        new_block_chain = BlockChain(block_data[0])

        second_block = Block(1, new_block_chain.blocks[0].hash, datetime.now(), block_data[1])
        second_block.hash = None
        new_block_chain.add_block(second_block)

        assert not new_block_chain.is_block_chain_valid()

    def test_create_block_chain_with_invalid_next_block_hash(self, block_data):
        new_block_chain = BlockChain(block_data[0])

        second_block = Block(1, new_block_chain.blocks[0].hash, datetime.now(), block_data[1])
        second_block.hash = "invalid hash"
        new_block_chain.add_block(second_block)

        assert not new_block_chain.is_block_chain_valid()

    def test_add_block_failed_when_block_chain_empty(self, block_data):
        new_block_chain = BlockChain()

        with pytest.raises(BlockChainNotInitializedError) as e:
            new_block_chain.add_block(new_block_chain.new_block(block_data[1]))

        assert e.value.code == "not-initialized"
        assert e.value.message == "BlockChain has not been initialized"

    def test_display_valid_block_chain(self, expected_result_block_chain, block_data):
        new_block_chain = BlockChain(block_data[0])

        new_block_chain.add_block(new_block_chain.new_block(block_data[1]))
        new_block_chain.add_block(new_block_chain.new_block(block_data[2]))
        new_block_chain.add_block(new_block_chain.new_block(block_data[3]))

        assert str(new_block_chain) == expected_result_block_chain(new_block_chain)

    def test_serialize_valid_block_chain(self, expected_serialized_block_chain, block_data):
        new_block_chain = BlockChain(block_data[0])

        new_block_chain.add_block(new_block_chain.new_block(block_data[1]))
        new_block_chain.add_block(new_block_chain.new_block(block_data[2]))
        new_block_chain.add_block(new_block_chain.new_block(block_data[3]))

        assert new_block_chain.serialize() == expected_serialized_block_chain(new_block_chain.blocks)

    def test_is_first_block_valid_return_true(self, block_data):
        new_block_chain = BlockChain(block_data[0])

        assert new_block_chain.is_first_block_valid()

    def test_is_first_block_valid_return_true_when_empty(self):
        new_block_chain = BlockChain()

        assert new_block_chain.is_first_block_valid()

    def test_is_block_chain_valid_return_true_when_empty(self):
        new_block_chain = BlockChain()

        assert new_block_chain.is_block_chain_valid()

    def test_init_from_list_of_dict_ok(self, block_chain_json, block_data):

        with open(block_chain_json) as json_file:
            block_chain = json.load(json_file)

        new_block_chain = BlockChain()
        new_block_chain.init_from_list_of_dict(block_chain)

        for index, block in enumerate(new_block_chain.blocks):
            if index == 0:
                assert block.index == index
                assert not block.previous_hash
                assert isinstance(block.hash, str)
                assert block.data == block_data[index]
            else:
                assert block.index == index
                assert block.previous_hash == new_block_chain.blocks[index - 1].hash
                assert isinstance(block.hash, str)
                assert block.data == block_data[index]

    def test_init_from_list_of_dict_failed_when_invalid_blockchain(self, block_chain_json):

        with open(block_chain_json) as json_file:
            block_chain = json.load(json_file)

        block_chain[0]["index"] = 10

        new_block_chain = BlockChain()

        with pytest.raises(BlockChainInvalid) as e:
            new_block_chain.init_from_list_of_dict(block_chain)

        assert e.value.code == "invalid-blockchain"
        assert e.value.message == "Blockchain  invalid"

    def test_init_from_list_of_dict_failed_when_invalid_json(self):

        block_chain = [
            "first block",
            "second block"
        ]

        new_block_chain = BlockChain()

        with pytest.raises(BlockChainInvalidList) as e:
            new_block_chain.init_from_list_of_dict(block_chain)

        assert e.value.code == "invalid-list"
        assert e.value.message == "Invalid list to create blockchain"

        block_chain = [
            {
                "data": "test"
            }
        ]

        new_block_chain = BlockChain()

        with pytest.raises(BlockChainInvalidList) as e:
            new_block_chain.init_from_list_of_dict(block_chain)

        assert e.value.code == "invalid-list"
        assert e.value.message == "Invalid list to create blockchain"

        block_chain = [
            {
                "index": 0
            }
        ]

        new_block_chain = BlockChain()

        with pytest.raises(BlockChainInvalidList) as e:
            new_block_chain.init_from_list_of_dict(block_chain)

        assert e.value.code == "invalid-list"
        assert e.value.message == "Invalid list to create blockchain"
