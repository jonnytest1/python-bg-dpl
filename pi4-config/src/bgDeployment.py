from ctypes import Union
from servicebase import BaseService
from services import serviceList
from customlogging import LogLevel, logKibana
from asyncEventHandler import AsyncEventHandler, EventIterator
from ServiceCl import ServiceCl
from FileChangeEvent import FileChangeEvent
from typing import Coroutine, List, Union
import asyncio
from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver
import debugpy
from dotenv import load_dotenv

print("python start")
try:
    debugpy.listen(("0.0.0.0", 5678))
    print("Waiting for debugger attach")
except:
    debugpy.listen(("0.0.0.0", 5679))
    print("Waiting for debugger attach on fallback port 5679")
    pass
load_dotenv()
observerList: "list[BaseObserver]" = []

loop = asyncio.get_event_loop()
queue = asyncio.Queue(loop=loop)


async def consume(queue: asyncio.Queue):
    async for event in EventIterator(queue):
        evt: FileChangeEvent = event

        try:
            print("queue item"+evt.path)
            task = loop.create_task(evt.service.triggerChange(evt.path))
            await task
        except Exception as e:
            logKibana(LogLevel.ERROR, "error in handling task",
                      e=e, args=dict(path=evt.path))

    logKibana(LogLevel.ERROR, "event loop stopped")


def watch(service: BaseService, queue: asyncio.Queue, loop: asyncio.BaseEventLoop):
    # Watch directory for changes
    handler = AsyncEventHandler(service, queue, loop)

    observer = Observer()
    observer.schedule(handler, service.folder_path, recursive=True)
    observer.start()
    logKibana(LogLevel.INFO, "observer started",
              args=dict(path=service.folder_path))


futureList: List[Union[asyncio.Future, Coroutine]] = [
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
except Exception as e:
    logKibana(LogLevel.ERROR, "got exception", e=e)
