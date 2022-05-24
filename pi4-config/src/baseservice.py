from xmlrpc.client import Boolean


class BaseService:

    def __init__(self, path: str, pattern: str):
        self.folder_path = path
        self.pattern = pattern

    async def triggerChange(self, path: str) -> Boolean:
        # interface method
        raise NotImplementedError("missing implementation for triggerChange")
