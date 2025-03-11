"""Custom defined exceptions file.
"""

class DataBaseEngineException(Exception):
    """Raised when configuring db engine at localhost
    """
    def __init__(self, msg: str):
        super().__init__(msg)
