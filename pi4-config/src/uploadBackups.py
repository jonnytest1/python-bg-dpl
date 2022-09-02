
import asyncio
import os
from os.path import isdir, join, isfile
from servicebackup import BackupService
from services import serviceList


async def recurseFolder(folder: str, service: BackupService):
    entries = os.listdir(folder)
    for entry in entries:
        path = join(folder, entry)
        if isdir(path):
            await recurseFolder(path, service)
        elif isfile(path):
            print(path)
            await service.triggerChange(path)


async def run():
    for service in serviceList:
        if isinstance(service, BackupService):
            await recurseFolder(service.folder_path, service)

if __name__ == "__main__":
    asyncio.run(run())
