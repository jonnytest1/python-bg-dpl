import re
from customlogging import LogLevel, logKibana

from dockerInstance import DockerInstance

from services import serviceList
data = '--publish "0.0.0.0:15748:4747/tcp" \\   --publish "0.0.0.0:15748:4747/tcp" \\'

repl = re.sub(r'--publish "0.0.0.0:([0-9]*):([0-9]*)/t',
              r'+-publish "0.0.0.0:20000-30000:\g<2>/t', data)

print(repl)


instance = DockerInstance(
    "d33455c698f3        jonathanheindl/rpi-nodets          \"/bin/sh -c /node.sh\"    2 months ago        Up 11 hours         0.0.0.0:15748->4747/tcp, 0.0.0.0:17935->8080/tcp                           docker_mapserver_1")
print(instance.image)
print(instance.name)


changed = serviceList[0].triggerChange(
    "/var/www/mapserver/mapserver/public/nue-script.js")
print(f"changed {changed}")


#logKibana(LogLevel.ERROR, "test")
