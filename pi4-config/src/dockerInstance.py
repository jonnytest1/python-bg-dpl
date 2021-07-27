
import re
import os
from typing import List
from requests import status_codes
import time

from dockerService import getRunCommand, getStatusForContainer, get_all_instances


class DockerInstance:
    name: str
    image: str

    dockerRunCommand: str

    ports: List[int] = None

    def __init__(self, outPutLine: str = None, name: str = None, image: str = None, runCommand: str = None):
        self.image = image
        self.name = name
        self.dockerRunCommand = runCommand
        if not outPutLine == None:
            self.parseOutPutLine(outputLine=outPutLine)

    def parseOutPutLine(self, outputLine):
        parts = re.split("[ ]{2,}", outputLine,)
        self.name = parts[6]
        self.image = parts[1]
        ports = parts[5].split(",")
        self.ports = []
        for port in ports:
            self.ports.append(port.split(":")[1].split("->")[0])

    def loadPorts(self):
        portString = getStatusForContainer(self.name)
        self.parseOutPutLine(portString)

    def getRunCommand(self):
        if self.dockerRunCommand is None:
            self.dockerRunCommand = getRunCommand(self.name)
        return self.dockerRunCommand

    def deploy(self, additionalEnvs: List[str]):
        command = self.getRunCommand()

        for env in additionalEnvs:
            print(f"adding {env}")
            command = command.replace(
                "--env", f"--env \"{env}=TRUE\" \\\n\t--env", 1)

        stream = os.popen(command)
        output = stream.read()

        if not len(output) == 65:
            raise SystemError(f"{len(output)}  {output}")

    def forNewInstance(self, name: str, instanceList: List["DockerInstance"]):
        replacedPorts = re.sub(r'--publish "0.0.0.0:([0-9]*):([0-9]*)/t',
                               r'--publish "0.0.0.0:20000-30000:\g<2>/t', self.getRunCommand())

        suffix = 2
        for instance in instanceList:
            try:
                index = int(instance.name.split("_").pop())
            except ValueError:
                index = 0

            if index >= suffix:
                suffix = index+1

        newName = f"{name}_{suffix}"

        print(len(instanceList))
        print(newName)
        replacedName = re.sub(
            r'--name "/(.*)"', f'--name "/{newName}"', replacedPorts)

        return DockerInstance(name=newName, image=self.image, runCommand=replacedName)

    @staticmethod
    def getAll():
        return list(map(lambda l: DockerInstance(outPutLine=l), get_all_instances()))
