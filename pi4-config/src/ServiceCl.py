from os import system
from HealthCheck import HealthCheck
from customlogging import LogLevel, logKibana
from dockerInstance import DockerInstance
import re
from nginxService import NginxService

allinstances = []


class ServiceCl:

    instances = []

    reloading = False

    def __init__(self, folderPath: str, pattern: str, dockerName: str, blackListPattern: str, healthcheckPath: str, envDictionary: dict, internOnly=False):
        self.folderPath = folderPath
        self.pattern = pattern
        self.dockerName = dockerName
        self.blacklistPattern = blackListPattern
        self.healthcheckPath = healthcheckPath
        self.envDictionary = envDictionary
        self.internOnly = internOnly

    async def triggerChange(self, path):
        try:
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
        except Exception as exc:
            logKibana(
                LogLevel.ERROR, f"error restarting container {self.dockerName}", exc, dict(
                    path=path,
                    fPath=self.folderPath,
                    healthPath=self.healthcheckPath
                ))
            raise exc

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
        envs = dict()
        for key, value in self.envDictionary.items():
            match = re.match(value, path)
            if not match == None:
                envs.setdefault(key, True)
            else:
                envs.setdefault(key, False)

        return envs

    async def restart(self, path: str):
        global allinstances

        instance = self.getCurrentInstance()
        print(f"current instance name {instance.name}")
        # prefetch for cache
        instance.getRunCommand()
        newInstance = instance.forNewInstance(
            self.dockerName, self.instances+allinstances)
        self.instances.append(newInstance)
        environments = self.getEnvForPath(path)
        newInstance.deploy(environments)

        await HealthCheck().checkHealthy(self.healthcheckPath, newInstance)
        logKibana(LogLevel.INFO,
                  f"new container {newInstance.name} is healthy")
        NginxService().updateConfig(self, newInstance)
        # running on new container

        logKibana(LogLevel.INFO,
                  f"switched to new container {newInstance.name}")

        instance.remove()
        instance.deploy(environments)
        await HealthCheck().checkHealthy(self.healthcheckPath, instance)
        logKibana(LogLevel.INFO,
                  f"restartet container {instance.name} is healthy")
        NginxService().updateConfig(self, instance)
        logKibana(LogLevel.INFO,
                  f"switched back to main container {instance.name}")

        newInstance.remove()
        logKibana(LogLevel.INFO,
                  f"cleaned up {newInstance.name}")
