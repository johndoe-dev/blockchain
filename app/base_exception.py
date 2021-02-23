class CustomBaseException(Exception):
    def __init__(self, message: str = None):
        self._message = message


