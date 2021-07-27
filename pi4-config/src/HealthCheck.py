import asyncio
import requests
from customlogging import LogLevel, logKibana

from dockerInstance import DockerInstance


class HealthCheck:

    async def checkHealthy(self, healthCheckUrl: str, instance: 'DockerInstance'):
        requestUtl = self.getRequestUrl(
            healthCheckUrl=healthCheckUrl, instance=instance)
        while not self.doHealthCheck(url=requestUtl):
            await asyncio.sleep(1)
            continue

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

        for i in range(len(instance.ports)):
            requestUrl = requestUrl.replace(f"[{i}]", instance.ports[i])

        return f"http://localhost:{requestUrl}"
