
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class BaseService:

    def __init__(self, path: str, pattern: str):
        self.folder_path = path
        self.pattern = pattern

    async def triggerChange(self, path: str) -> bool:
        # interface method
        raise NotImplementedError("missing implementation for triggerChange")
