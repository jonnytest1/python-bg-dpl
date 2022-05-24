import asyncio
from msilib.schema import Error
import requests
from customlogging import LogLevel, logKibana
from enum import Enum
from dockerInstance import DockerInstance
from datetime import datetime, timedelta


class HealthStatus(Enum):
    Healthy = "Healthy"
    UnHealthy = "UnHealthy"


class HealthCheck:

    healthchecktimeout = 2

    async def checkHealthy(self, healthCheckUrl: str, instance: 'DockerInstance') -> HealthStatus:
        requestUtl = self.getRequestUrl(
            healthCheckUrl=healthCheckUrl, instance=instance)
        start = datetime.now()

        while not self.doHealthCheck(url=requestUtl):
            await asyncio.sleep(1)
            if start < (datetime.now() - timedelta(minutes=HealthCheck.healthchecktimeout)):
                return HealthStatus.UnHealthy
            continue

        return HealthStatus.Healthy

    def doHealthCheck(self, url: str):
        print(f"checking url at {url}")
        try:
            response = requests.get(url)
            return response.status_code >= 200 and response.status_code < 400
        except requests.ConnectionError:
            return False

    def getRequestUrl(self, healthCheckUrl: str, instance: 'DockerInstance'):
        requestUrl = healthCheckUrl

        if instance.ports == None:
            instance.loadPorts()
        if instance.ports == None:
            raise Exception("couldnt load ports")
        for i in range(len(instance.ports)):
            requestUrl = requestUrl.replace(f"[{i}]", str(instance.ports[i]))

        return f"http://localhost:{requestUrl}"
