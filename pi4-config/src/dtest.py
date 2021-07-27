from service import Service
from services import serviceList


service = serviceList[0]
instance = service.getCurrentInstance()
# print(instance.getRunCommand())

newInstance = instance.forNewInstance(service.dockerName, service.instances)
service.instances.append(newInstance)
# print(newInstance.getRunCommand())

newInstance = instance.forNewInstance(service.dockerName, service.instances)
service.instances.append(newInstance)
print(newInstance.getRunCommand())

# newInstance.checkHealthy(service.healthcheckPath)
service.restart()
# newInstance.deploy()