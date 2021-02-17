import pytest
from app import Block, BlockChain, BlockChainException
from datetime import datetime


class TestBlock:

    def test_create_block(self):
        new_block = Block(0, None, datetime.now(), "test block")

        assert new_block.index == 0
        assert not new_block.previous_hash
        assert isinstance(new_block.hash, str)
        assert new_block.data

    def test_serialize(self, expected_serialized_block):
        new_block = Block(0, None, datetime.now(), "test block")

        assert new_block.serialize() == expected_serialized_block(new_block)


class TestBlockChain:

    def teardown_method(self):
        BlockChain.blocks = []

    def test_create_block_chain_with_first_block_ok(self):
        new_block_chain = BlockChain("first block")
        assert len(new_block_chain.blocks) == 1
        assert new_block_chain.is_block_chain_valid()

        first_block = new_block_chain.blocks[0]

        assert first_block.index == 0
        assert not first_block.previous_hash
        assert isinstance(first_block.hash, str)
        assert first_block.data == "first block"

    def test_init_first_ok(self):
        new_block_chain = BlockChain()
        new_block_chain.init_first("first block")

        assert len(new_block_chain.blocks) == 1

        first_block = new_block_chain.blocks[0]

        assert first_block.index == 0
        assert not first_block.previous_hash
        assert isinstance(first_block.hash, str)
        assert first_block.data == "first block"

    def test_init_first_fail_when_first_block_already_exist(self):
        new_block_chain = BlockChain("first block")

        with pytest.raises(BlockChainException):
            new_block_chain.init_first("first block")

    def test_create_block_chain_with_several_blocks_ok(self):
        new_block_chain = BlockChain("first block")

        new_block_chain.add_block(new_block_chain.new_block("Second Block"))
        new_block_chain.add_block(new_block_chain.new_block("third Block"))
        new_block_chain.add_block(new_block_chain.new_block("fourth Block"))

        expected_data = ["first block", "Second Block", "third Block", "fourth Block"]

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

    def test_create_block_chain_with_first_block_invalid_index(self):
        new_block_chain = BlockChain("first block")

        bad_first_block = Block(10, None, datetime.now(), "first block")

        new_block_chain.blocks[0] = bad_first_block

        assert not new_block_chain.is_block_chain_valid()

    def test_create_block_chain_with_first_block_invalid_previous_hash(self):
        new_block_chain = BlockChain("first block")

        bad_first_block = Block(0, "0OIJKjkghjbgghu", datetime.now(), "first block")

        new_block_chain.blocks[0] = bad_first_block

        assert not new_block_chain.is_block_chain_valid()

    def test_create_block_chain_with_first_block_invalid_hash(self):
        new_block_chain = BlockChain("first block")

        bad_first_block = Block(0, None, datetime.now(), "first block")
        bad_first_block.hash = "1234"

        new_block_chain.blocks[0] = bad_first_block

        assert not new_block_chain.is_block_chain_valid()

    def test_create_block_chain_with_invalid_next_block_index(self):
        new_block_chain = BlockChain("first block")

        second_block = Block(2, new_block_chain.blocks[0].hash, datetime.now(), "second block")
        new_block_chain.add_block(second_block)

        assert not new_block_chain.is_block_chain_valid()

    def test_create_block_chain_with_invalid_next_block_previous_hash(self):
        new_block_chain = BlockChain("first block")

        second_block = Block(1, "bad previous hash", datetime.now(), "second block")
        new_block_chain.add_block(second_block)

        assert not new_block_chain.is_block_chain_valid()

    def test_create_block_chain_with_invalid_next_block_hash(self):
        new_block_chain = BlockChain("first block")

        second_block = Block(1, new_block_chain.blocks[0].hash, datetime.now(), "second block")
        second_block.hash = None
        new_block_chain.add_block(second_block)

        assert not new_block_chain.is_block_chain_valid()

    def test_display_valid_block_chain(self, expected_result_block_chain):
        new_block_chain = BlockChain("first block")

        new_block_chain.add_block(new_block_chain.new_block("second block"))
        new_block_chain.add_block(new_block_chain.new_block("third block"))
        new_block_chain.add_block(new_block_chain.new_block("fourth block"))

        assert str(new_block_chain) == expected_result_block_chain(new_block_chain)

    def test_serialize_valid_block_chain(self, expected_serialized_block_chain):
        new_block_chain = BlockChain("first block")

        new_block_chain.add_block(new_block_chain.new_block("second block"))
        new_block_chain.add_block(new_block_chain.new_block("third block"))
        new_block_chain.add_block(new_block_chain.new_block("fourth block"))

        assert new_block_chain.serialize() == expected_serialized_block_chain(new_block_chain.blocks)
