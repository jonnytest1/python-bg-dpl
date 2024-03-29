#from nginxService import NginxService
#from ServiceCl import ServiceCl
from ServiceCl import ServiceCl
from services import serviceList


service = serviceList[0]
if not isinstance(service, ServiceCl):
    raise Exception("error")

instance = service.getCurrentInstance()

if instance == None:
    raise Exception("error")
# print(instance.getRunCommand())

#newInstance = instance.forNewInstance(service.dockerName, service.instances)
# service.instances.append(newInstance)
# print(newInstance.getRunCommand())

newInstance = instance.forNewInstance(service.dockerName, service.instances)
service.instances.append(newInstance)
print(newInstance.get_run_command())
command = newInstance.get_run_command()

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
