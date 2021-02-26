import pytest
from app.blockchain_api.exceptions import DataMissingKeyError, DataTypeError


class TestDataMissingKeyError:
    def test_data_missing_key_error(self):
        with pytest.raises(DataMissingKeyError) as e:
            raise DataMissingKeyError

        assert e.value.message == "Data miss some keys"
        assert e.value.code == "missing-key-error"

    def test_data_missing_key_error_with_message(self):
        with pytest.raises(DataMissingKeyError) as e:
            raise DataMissingKeyError("Fake message")

        assert e.value.message == "Fake message"
        assert e.value.code == "missing-key-error"


class TestDataTypeError:
    def test_data_type_error(self):
        with pytest.raises(DataTypeError) as e:
            raise DataTypeError

        assert e.value.message == "Data has bad type"
        assert e.value.code == "data-type-error"

    def test_data_type_error_with_message(self):
        with pytest.raises(DataTypeError) as e:
            raise DataTypeError("Fake message")

        assert e.value.message == "Fake message"
        assert e.value.code == "data-type-error"
