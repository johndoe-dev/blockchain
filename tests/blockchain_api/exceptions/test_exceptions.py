import pytest
from app.blockchain_api.exceptions import DataMissingKeyError


class TestDataMissingKeyError:
    def test_block_chain_not_initialized_error(self):
        with pytest.raises(DataMissingKeyError) as e:
            raise DataMissingKeyError

        assert e.value.message == "Data miss some keys"
        assert e.value.code == "missing-key-error"

    def test_block_chain_not_initialized_error_with_message(self):
        with pytest.raises(DataMissingKeyError) as e:
            raise DataMissingKeyError("Fake message")

        assert e.value.message == "Fake message"
        assert e.value.code == "missing-key-error"
