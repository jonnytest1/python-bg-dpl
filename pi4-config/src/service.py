from customlogging import LogLevel, logKibana
from dockerService import get_all_instances, healthcheck, run_docker
from nginxService import reloadConfig, setConfig
import re

allinstances = []


class Service:

    instances = []

    def __init__(self, folderPath: str, pattern: str, dockerName: str, blackListPattern: str, healthcheckPath: str):
        self.folderPath = folderPath
        self.pattern = pattern
        self.dockerName = dockerName
        self.blacklistPattern = blackListPattern
        self.healthcheckPath = healthcheckPath

    def triggerChange(self, path):
        if (not self.blacklistPattern == None) and (not re.match(f".*{self.blacklistPattern}.*", path) == None):
            print(f"{path} filtered by blacklist {self.blacklistPattern}")
            return False
        print(f"change in {self.dockerName}")
        self.restart()
        return True

    def getCurrentInstance(self):
        global allinstances
        allinstances = get_all_instances()

        for instance in allinstances:
            if instance.name.startswith(self.dockerName):
                return instance

        logKibana(level=LogLevel.ERROR,
                  msg="didnt find instance with service name")
        return None

    def restart(self):
        global allinstances
        instance = self.getCurrentInstance()
        print(allinstances)
        newInstance = instance.forNewInstance(
            self.dockerName, self.instances+allinstances)
        self.instances.append(newInstance)
        newInstance.deploy()
        newInstance.checkHealthy(self.healthcheckPath)
        # run_docker()
        # healthcheck()
       # setConfig()
        # reloadConfig()
