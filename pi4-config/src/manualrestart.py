
import asyncio
import sys
from services import serviceList
print(sys.argv)


serviceIndexArgument = sys.argv[1]
serviceIndex = int(serviceIndexArgument)
service = serviceList[serviceIndex]


print(service.dockerName)


async def restartService():
    print(f"restarting {service.dockerName} in 2 seconds ")
    await asyncio.sleep(2)
    await service.restart("")


if service != None:
    asyncio.run(restartService())
