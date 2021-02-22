class BlockChainException(Exception):
    def __init__(self, message: str = None):
        self._message = message


class BlockChainAlreadyInitError(BlockChainException):
    @property
    def code(self):
        return "already-initialized"

    @property
    def message(self):
        if self._message:
            return self._message
        return "BlockChain already initialized"


class BlockChainNotInitializedError(BlockChainException):
    @property
    def code(self):
        return "not-initialized"

    @property
    def message(self):
        if self._message:
            return self._message
        return "BlockChain has not been initialized"


class BlockChainDataInvalid(BlockChainException):
    @property
    def code(self):
        return "invalid-data"

    @property
    def message(self):
        if self._message:
            return self._message
        return "Invalid data received to create a block"


class BlockChainInvalid(BlockChainException):
    @property
    def code(self):
        return "invalid-blockchain"

    @property
    def message(self):
        if self._message:
            return self._message
        return "Blockchain  invalid"


class BlockChainInvalidList(BlockChainException):
    @property
    def code(self):
        return "invalid-list"

    @property
    def message(self):
        if self._message:
            return self._message
        return "Invalid list to create blockchain"
