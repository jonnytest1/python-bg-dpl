#from nginxService import NginxService
#from ServiceCl import ServiceCl
from services import serviceList


service = serviceList[0]
instance = service.getCurrentInstance()
# print(instance.getRunCommand())

#newInstance = instance.forNewInstance(service.dockerName, service.instances)
# service.instances.append(newInstance)
# print(newInstance.getRunCommand())

newInstance = instance.forNewInstance(service.dockerName, service.instances)
service.instances.append(newInstance)
print(newInstance.getRunCommand())
command = newInstance.getRunCommand()

for key, value in dict(SKIP_NPM=False).items():
    if value == True:
        print(f"adding {key}")
        command = command.replace(
            "--env", f"--env \"{key}=TRUE\" \\\n\t--env", 1)
    else:
        print(f"removin {key}")
        command = command.replace(f"--env \"{key}=TRUE\" \\\n  ", "")

print(command)


# newInstance.checkHealthy(service.healthcheckPath)
# service.restart()
# newInstance.deploy()
#NginxService().setConfig(service, instance=instance)
