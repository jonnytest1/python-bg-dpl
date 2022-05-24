
import asyncio
from datetime import datetime
import sys
from ServiceCl import ServiceCl
from services import serviceList
print(sys.argv)


serviceIndexArgument = sys.argv[1]
serviceIndex = int(serviceIndexArgument)
service = serviceList[serviceIndex]

if not isinstance(service, ServiceCl):
    raise Exception("wrong instance")
print(service.dockerName)


async def restartService():
    print(f"restarting {service.dockerName} in 2 seconds ")
    await asyncio.sleep(2)
    await service.restart("", datetime.now())


if service != None:
    asyncio.run(restartService())
