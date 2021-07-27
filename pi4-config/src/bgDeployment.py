import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import asyncio
from typing import List
from FileChangeEvent import FileChangeEvent
from ServiceCl import ServiceCl
from asyncEventHandler import AsyncEventHandler, EventIterator
from services import serviceList
from pathlib import Path

observerList: List[Observer] = []

loop = asyncio.get_event_loop()
queue = asyncio.Queue(loop=loop)


async def consume(queue: asyncio.Queue) -> None:
    async for event in EventIterator(queue):
        evt: FileChangeEvent = event
        loop.create_task(evt.service.triggerChange(event.path))
    print("consumer")


def watch(service: ServiceCl, queue: asyncio.Queue, loop: asyncio.BaseEventLoop) -> None:
    """Watch a directory for changes."""
    handler = AsyncEventHandler(service, queue, loop)

    observer = Observer()
    observer.schedule(handler, service.folderPath, recursive=True)
    observer.start()
    print("Observer started")


futureList = [
    consume(queue)
]

for service in serviceList:
    futureList.append(loop.run_in_executor(None, watch, service, queue, loop))


try:
    loop.run_until_complete(asyncio.gather(*futureList))
except KeyboardInterrupt:
    loop.stop()
    for observer in observerList:
        observer.stop()
        observer.join()
