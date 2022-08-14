
import re
import os
from typing import List, Union

from dockerService import getContainerLogs, get_run_command, getStatusForContainer, get_all_instances, removeContainer, restartContainer
import json


class DockerInstance:
    name: str
    image: str

    docker_run_command: Union[str, None] = None

    ports: Union[List[int], None] = None

    aborted = False

    def __init__(self, outPutLine: Union[str, None] = None,
                 name: Union[str, None] = None, image: Union[str, None] = None,
                 runCommand: Union[str, None] = None):
        if image != None:
            self.image = image
        if name != None:
            self.name = name

        if runCommand != None:
            self.docker_run_command = runCommand
        if not outPutLine == None:
            self.parseOutPutLine(outputLine=outPutLine)

    def parseOutPutLine(self, outputLine):
        try:
            parts = re.split("[ ]{2,}", outputLine,)
            nameIndex = 6
            self.ports = []
            if "Exited" in outputLine:
                nameIndex = 5
            else:
                if not ("->" in parts[5]):
                    nameIndex = 5
                else:
                    ports = parts[5].split(",")
                    for port in ports:
                        # otherwise port is not mapped
                        if("->" in port):
                            self.ports.append(
                                int(port.split(":")[-1].split("->")[0]))
            self.name = parts[nameIndex].strip()
            self.image = parts[1]

        except Exception as e:
            print(outputLine)
            raise e

    def loadPorts(self):
        portString = getStatusForContainer(self.name)
        self.parseOutPutLine(portString)

    def get_run_command(self):
        if self.docker_run_command is None:
            self.docker_run_command = get_run_command(self.name)
        return self.docker_run_command

    def deploy(self, additionalEnvs: dict):
        command = self.get_run_command()

        for key, value in additionalEnvs.items():
            if value == True:
                print(f"adding {key}")
                command = command.replace(
                    "--env", f"--env \"{key}=TRUE\" \\\n\t--env", 1)
            else:
                command = command.replace(f"--env \"{key}=TRUE\" \\\n  ", "")

        stream = os.popen(command)
        output = stream.read()

        if not len(output) == 65:
            raise SystemError(f"{len(output)}  {output}")

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def forNewInstance(self, name: str, instanceList: List["DockerInstance"]):
        replacedPorts = re.sub(r'--publish "0.0.0.0:([0-9]*):([0-9]*)/t',
                               r'--publish "0.0.0.0:20000-30000:\g<2>/t', self.get_run_command())

        suffix = 2
        for instance in instanceList:
            try:
                index = int(instance.name.split("_").pop())
            except ValueError:
                index = 0

            if index >= suffix:
                suffix = index+1

        newName = f"{name}_{suffix}"

        print(newName)
        replacedName = re.sub(
            r'--name "/(.*)"', f'--name "/{newName}"', replacedPorts)

        return DockerInstance(name=newName, image=self.image, runCommand=replacedName)

    # def restart(self, envs: List[str]):
    #    print(f"container restarting {self.name}")
    #    restartContainer(self.name, envs)
    #   print("container restarted")

    def remove(self):
        removeContainer(self.name)
        print("container removed")

    def getLogs(self):
        return getContainerLogs(self.name)

    @staticmethod
    def getAll():
        return list(map(lambda l: DockerInstance(outPutLine=l), get_all_instances()))
