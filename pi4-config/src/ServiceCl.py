from HealthCheck import HealthCheck
from customlogging import LogLevel, logKibana
from dockerInstance import DockerInstance
import re
from nginxService import NginxService

allinstances = []


class ServiceCl:

    instances = []

    reloading = False

    def __init__(self, folderPath: str, pattern: str, dockerName: str, blackListPattern: str, healthcheckPath: str, envDictionary: dict):
        self.folderPath = folderPath
        self.pattern = pattern
        self.dockerName = dockerName
        self.blacklistPattern = blackListPattern
        self.healthcheckPath = healthcheckPath
        self.envDictionary = envDictionary

    async def triggerChange(self, path):
        if self.reloading == True:
            print(f"already relaoding for {path}")
            return
        self.reloading = True

        if (not self.blacklistPattern == None) and (not re.match(f".*{self.blacklistPattern}.*", path) == None):
            print(f"{path} filtered by blacklist {self.blacklistPattern}")
            return False
        logKibana(LogLevel.INFO, f"restarting for {self.dockerName}")
        await self.restart(path)
        self.reloading = False
        return True

    def getCurrentInstance(self):
        global allinstances
        allinstances = DockerInstance.getAll()

        for instance in allinstances:
            if instance.name.startswith(self.dockerName):
                return instance

        logKibana(level=LogLevel.ERROR,
                  msg="didnt find instance with service name")
        return None

    def getEnvForPath(self, path: str):
        envs = []
        for key, value in self.envDictionary.items():
            match = re.match(value, path)
            if not match == None:
                envs.append(key)

        return envs

    async def restart(self, path: str):
        global allinstances

        instance = self.getCurrentInstance()
        newInstance = instance.forNewInstance(
            self.dockerName, self.instances+allinstances)
        self.instances.append(newInstance)
        newInstance.deploy(self.getEnvForPath(path))

        await HealthCheck().checkHealthy(self.healthcheckPath, newInstance)

        NginxService().updateConfig(self, newInstance)

        # TODO:
        # restart old container for correct ports
