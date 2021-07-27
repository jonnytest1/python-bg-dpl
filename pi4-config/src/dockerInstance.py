import re
import os
from typing import List
import requests
from requests import status_codes
import time


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
        stream = os.popen(f'docker ps -a | grep -H {self.name}')
        portString = stream.read()
        self.parseOutPutLine(portString)

    def getRunCommand(self):
        if self.dockerRunCommand is None:
            stream = os.popen(
                'docker inspect --format "$(cat ./dockerrun.tpl)" '+self.name)
            self.dockerRunCommand = stream.read()
        return self.dockerRunCommand

    def deploy(self):
        stream = os.popen(self.getRunCommand())
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

    def checkHealthy(self, healthCheckUrl: str):
        requestUtl = self.getRequestUrl(healthCheckUrl=healthCheckUrl)
        while not self.doHealthCheck(url=requestUtl):
            time.sleep(1)
            continue

    def doHealthCheck(self, url: str):
        print(f"checking url at {url}")
        try:
            response = requests.get(url)
            print(response.status_code)
            return response.status_code >= 200 and response.status_code < 400
        except requests.ConnectionError:
            return False

    def getRequestUrl(self, healthCheckUrl: str):
        requestUrl = healthCheckUrl

        if self.ports == None:
            self.loadPorts()

        for i in range(len(self.ports)):
            requestUrl = requestUrl.replace(f"[{i}]", self.ports[i])

        return f"http://localhost:{requestUrl}"
