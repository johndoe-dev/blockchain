from app.base_exception import CustomBaseException


class BlockChainApiException(CustomBaseException):
    pass


class DataMissingKeyError(BlockChainApiException):
    @property
    def code(self):
        return "missing-key-error"

    @property
    def message(self):
        if self._message:
            return self._message
        return "Data miss some keys"


class DataTypeError(BlockChainApiException):
    @property
    def code(self):
        return "data-type-error"

    @property
    def message(self):
        if self._message:
            return self._message
        return "Data has bad type"


