import os
import re
from customlogging import LogLevel, logKibana
from dockerInstance import DockerInstance
import ServiceCl

nginxPath = "/etc/nginx/locations"


class NginxService:

    def updateConfig(self, service: "ServiceCl.ServiceCl", instance: "DockerInstance"):
        file = f"{nginxPath}/{service.dockerName}.locations"

        logKibana(LogLevel.INFO, "updating config")
        with open(file, "r") as myfile:
            data: str = myfile.read()
            healthcheckPortIndex = int(service.healthcheckPath[1])

            if not data.startswith("#auto-generated"):
                data = f"#auto-generated from python blue-green deployment for '{service.dockerName}'\n{data}"

            newConfig = re.sub(
                r"proxy_pass http://127\.0\.0\.1:([0-9]{3,5})", f"proxy_pass http://127.0.0.1:{instance.ports[healthcheckPortIndex]}", data)
        with open(file, "w") as myfile:
            myfile.write(newConfig)

        logKibana(LogLevel.INFO, "updating config",
                  None, dict(config=newConfig))
        self.reloadConfig()

    def reloadConfig(self):
        stream = os.popen("service nginx reload")
        output = stream.read()

        if len(output) > 0:
            statusStr = os.popen("systemctl status nginx.service")
            logKibana(LogLevel.ERROR, "nginx didnt start correctly",
                      None, args=dict(status=statusStr.read()))

        print("reloaded config")
