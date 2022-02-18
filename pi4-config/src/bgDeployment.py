from services import serviceList
from customlogging import LogLevel, logKibana
from asyncEventHandler import AsyncEventHandler, EventIterator
from ServiceCl import ServiceCl
from FileChangeEvent import FileChangeEvent
from typing import List
import asyncio
from watchdog.observers import Observer
import debugpy

debugpy.listen(("0.0.0.0", 5678))
print("Waiting for debugger attach")

observerList: List[Observer] = []

loop = asyncio.get_event_loop()
queue = asyncio.Queue(loop=loop)


async def consume(queue: asyncio.Queue):
    async for event in EventIterator(queue):
        evt: FileChangeEvent = event
        loop.create_task(evt.service.triggerChange(event.path))

    logKibana(LogLevel.ERROR, "event loop stopped")


def watch(service: ServiceCl, queue: asyncio.Queue, loop: asyncio.BaseEventLoop):
    # Watch directory for changes
    handler = AsyncEventHandler(service, queue, loop)

    observer = Observer()
    observer.schedule(handler, service.folderPath, recursive=True)
    observer.start()
    logKibana(LogLevel.INFO, "observer started")


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
