import ServiceCl


class FileChangeEvent:
    def __init__(self, service: ServiceCl.ServiceCl, path: str) -> None:
        self.service = service
        self.path = path
