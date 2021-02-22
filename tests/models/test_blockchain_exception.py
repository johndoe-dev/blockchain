import pytest
from app.models import (
    BlockChainNotInitializedError,
    BlockChainAlreadyInitError,
    BlockChainDataInvalid,
    BlockChainInvalid,
    BlockChainInvalidList)


class TestBlockChainNotInitializedError:
    def test_block_chain_not_initialized_error(self):
        with pytest.raises(BlockChainNotInitializedError) as e:
            raise BlockChainNotInitializedError

        assert e.value.message == "BlockChain has not been initialized"
        assert e.value.code == "not-initialized"

    def test_block_chain_not_initialized_error_with_message(self):
        with pytest.raises(BlockChainNotInitializedError) as e:
            raise BlockChainNotInitializedError("Fake message")

        assert e.value.message == "Fake message"
        assert e.value.code == "not-initialized"


class TestBlockChainAlreadyInitError:
    def test_block_chain_already_init_error(self):
        with pytest.raises(BlockChainAlreadyInitError) as e:
            raise BlockChainAlreadyInitError

        assert e.value.message == "BlockChain already initialized"
        assert e.value.code == "already-initialized"

    def test_block_chain_already_init_error_with_message(self):
        with pytest.raises(BlockChainAlreadyInitError) as e:
            raise BlockChainAlreadyInitError("Fake message")

        assert e.value.message == "Fake message"
        assert e.value.code == "already-initialized"


class TestBlockChainDataInvalid:
    def test_block_chain_data_invalid(self):
        with pytest.raises(BlockChainDataInvalid) as e:
            raise BlockChainDataInvalid

        assert e.value.message == "Invalid data received to create a block"
        assert e.value.code == "invalid-data"

    def test_block_chain_data_invalid_with_message(self):
        with pytest.raises(BlockChainDataInvalid) as e:
            raise BlockChainDataInvalid("Fake message")

        assert e.value.message == "Fake message"
        assert e.value.code == "invalid-data"


class TestBlockChainInvalid:
    def test_block_chain_invalid(self):
        with pytest.raises(BlockChainInvalid) as e:
            raise BlockChainInvalid

        assert e.value.message == "Blockchain  invalid"
        assert e.value.code == "invalid-blockchain"

    def test_block_chain_invalid_with_message(self):
        with pytest.raises(BlockChainInvalid) as e:
            raise BlockChainInvalid("Fake message")

        assert e.value.message == "Fake message"
        assert e.value.code == "invalid-blockchain"


class TestBlockChainInvalidJson:
    def test_block_chain_invalid(self):
        with pytest.raises(BlockChainInvalidList) as e:
            raise BlockChainInvalidList

        assert e.value.message == "Invalid list to create blockchain"
        assert e.value.code == "invalid-list"

    def test_block_chain_invalid_with_message(self):
        with pytest.raises(BlockChainInvalidList) as e:
            raise BlockChainInvalidList("Fake message")

        assert e.value.message == "Fake message"
        assert e.value.code == "invalid-list"
