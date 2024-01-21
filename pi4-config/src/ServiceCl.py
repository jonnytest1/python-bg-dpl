import asyncio
from datetime import datetime
from HealthCheck import HealthCheck, HealthStatus
from servicebase import BaseService
from customlogging import LogLevel, logKibana
from dockerInstance import DockerInstance
import re
from nginxService import NginxService
import jsonpickle
allinstances = []


class ServiceCl(BaseService):

    instances = []

    reloading = False

    lastTrigger = datetime.fromtimestamp(0)

    def __init__(self, folder_path: str, pattern: str, dockerName: str, blackListPattern: str, healthcheckPath: str, envDictionary: dict, internOnly=False):
        super().__init__(folder_path, pattern)
        self.dockerName = dockerName
        self.blacklistPattern = blackListPattern
        self.healthcheckPath = healthcheckPath
        self.envDictionary = envDictionary
        self.internOnly = internOnly

    async def triggerChange(self, path):
        try:
           # if self.reloading == True:
            # logKibana(LogLevel.INFO,
            #          f"already relaoding {self.dockerName} for {path}")
            # return
           # self.reloading = True
            trigger = datetime.now()
            if (not self.blacklistPattern == None) and (not re.match(f".*{self.blacklistPattern}.*", path) == None):
                logKibana(LogLevel.DEBUG, "blacklisted file change event", args=dict(
                    file=path,
                    blacklist_pattern=self.blacklistPattern
                ))
                return False
            self.lastTrigger = trigger
            logKibana(LogLevel.DEBUG, "file change event",
                      args=dict(file=path))
            await self.restart(path, trigger)
            self.reloading = False
            return True
        except Exception as exc:
            self.reloading = False
            logKibana(
                LogLevel.ERROR, f"error restarting container {self.dockerName}", exc, dict(
                    path=path,
                    fPath=self.folder_path,
                    healthPath=self.healthcheckPath
                ))
            raise exc

    def getCurrentInstance(self):
        global allinstances
        allinstances = DockerInstance.getAll()

        for instance in allinstances:
            if instance.name == self.dockerName or instance.name == self.dockerName+"_1":
                return instance

        logKibana(level=LogLevel.ERROR,
                  msg="didnt find instance with service name", args=dict(
                      instances=jsonpickle.encode(allinstances),
                      dockerName=self.dockerName
                  ))
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

    async def restart(self, path: str, eventTime: datetime):
        global allinstances

        instance = self.getCurrentInstance()
        if instance == None:
            logKibana(
                LogLevel.ERROR, f"didnt get current instance for {self.dockerName}",
            )
            return
        logKibana(
                LogLevel.INFO, f"restarting container {self.dockerName}",
            )
        print(f"current instance name {instance.name}")
        # prefetch for cache
        instance.get_run_command()
        newInstance = instance.forNewInstance(
            self.dockerName, self.instances+allinstances)
        self.instances.append(newInstance)
        environments = self.getEnvForPath(path)
        await asyncio.sleep(0.5)
        print("waited for new event")
        if(self.lastTrigger != eventTime):
            logKibana(
                LogLevel.DEBUG, "skipped restart because other event triggered shortly after")
            return
        newInstance.deploy(environments)

        healthStatus = await HealthCheck().checkHealthy(self.healthcheckPath, newInstance)
        if healthStatus == HealthStatus.UnHealthy:
            self.reloading = False
            logKibana(
                LogLevel.ERROR, f"new container {newInstance.name} is unhealthy after {HealthCheck.healthchecktimeout} minutes",
                args=dict(logoutput=newInstance.getLogs()))
            newInstance.remove()
            return
        if self.lastTrigger != eventTime:
            logKibana(
                LogLevel.DEBUG, "skipped restart because other event triggered shortly after health check of new container", args=dict(logoutput=newInstance.getLogs()))
            newInstance.remove()
            return

        logKibana(LogLevel.INFO,
                  f"new container {newInstance.name} is healthy")
        if not NginxService().updateConfig(self, newInstance):
            return
        # running on new container

        logKibana(LogLevel.INFO,
                  f"switched to new container {newInstance.name}")

        instance.remove()
        instance.deploy(environments)
        
        swithcedBackSTatus=await HealthCheck().checkHealthy(self.healthcheckPath, instance)

        if swithcedBackSTatus == HealthStatus.UnHealthy:
            logKibana(
                LogLevel.ERROR, f"switched back container {instance.name} is unhealthy after {HealthCheck.healthchecktimeout} minutes",
                args=dict(logoutput=instance.getLogs()))
        logKibana(LogLevel.INFO,
                  f"restartet container {instance.name} is healthy")

        if self.lastTrigger == eventTime:
            if not NginxService().updateConfig(self, instance):
                return
        else:
            logKibana(LogLevel.WARNING,
                      f"lasttrigger not event time after healthy", None, dict(last_trigger=self.lastTrigger, event_time=eventTime))

        logKibana(LogLevel.INFO,
                  f"switched back to main container {instance.name}")

        newInstance.remove()
        logKibana(LogLevel.INFO,
                  f"cleaned up {newInstance.name}")
