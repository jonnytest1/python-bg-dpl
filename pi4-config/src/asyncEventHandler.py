from typing import Optional
from watchdog.events import FileSystemEvent, PatternMatchingEventHandler
import asyncio
from FileChangeEvent import FileChangeEvent

from ServiceCl import ServiceCl
from customlogging import LogLevel, logKibana


class AsyncEventHandler(PatternMatchingEventHandler):

    def __init__(self, service: ServiceCl, queue: asyncio.Queue,
                 loop: Optional[asyncio.BaseEventLoop] = None):
        self.queue = queue
        self.service = service
        self.loop = loop
        super().__init__(patterns=[service.pattern],
                         ignore_patterns=None, ignore_directories=True, case_sensitive=True)

    def addToQueue(self, path):
        logKibana(LogLevel.INFO, "file change event")
        self.loop.call_soon_threadsafe(
            self.queue.put_nowait, FileChangeEvent(path=path, service=self.service))

    def on_created(self, event: FileSystemEvent):
        self.addToQueue(event.src_path)

    def on_deleted(self, event):
        self.addToQueue(event.src_path)

    def on_modified(self, event):
        self.addToQueue(event.src_path)

    def on_moved(self, event):
        self.addToQueue(event.src_path)
        self.addToQueue(event.dest_path)


class EventIterator(object):
    def __init__(self, queue: asyncio.Queue,
                 loop: Optional[asyncio.BaseEventLoop] = None):
        self.queue = queue

    def __aiter__(self):
        return self

    async def __anext__(self):
        item = await self.queue.get()

        if item is None:
            logKibana(LogLevel.ERROR, "None in event loop")
            raise StopAsyncIteration

        return item
