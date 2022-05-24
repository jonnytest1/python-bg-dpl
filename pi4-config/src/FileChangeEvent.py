from baseservice import BaseService


class FileChangeEvent:
    def __init__(self, service: BaseService, path: str) -> None:
        self.service = service
        self.path = path
