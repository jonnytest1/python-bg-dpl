from datetime import date, datetime
import json
from HealthCheck import HealthCheck
from customlogging import LogLevel, logKibana
from dockerInstance import DockerInstance
import re
from services import serviceList
# logKibana(LogLevel.DEBUG, "test")


instance = DockerInstance(
    outPutLine='122b6725fd0d   jonathanheindl/rpi-nodets          "/bin/sh -c /node.sh"    10 hours ago   Up 9 hours                                                                                         docker_sound')

if not instance.name == "docker_sound":
    raise Exception("failed parsing")
if not instance.image == "jonathanheindl/rpi-nodets":
    raise Exception("failed parsing")

smInst = DockerInstance(
    'f5de15bbe3b9   jonathanheindl/rpi-nodets:latest   "/bin/sh -c /node.sh"    18 hours ago   Up 18 hours   0.0.0.0:1880->1880/tcp, 0.0.0.0:14747->4747/tcp, 0.0.0.0:16934->8080/tcp             docker_smarthome')
if not smInst.name == "docker_smarthome":
    raise Exception("failed parsing")

if not smInst.image == "jonathanheindl/rpi-nodets:latest":
    raise Exception("failed parsing")
if smInst.ports == None or len(smInst.ports) != 3:
    raise Exception("failed parsing")

test = f"new container {instance.name} is unhealthy after {HealthCheck.healthchecktimeout} minutes"
print(re.sub("test", "123", "testdef\nabc\ntesthij"))
