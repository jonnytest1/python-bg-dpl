import os
import re
from customlogging import LogLevel, logKibana
from dockerInstance import DockerInstance
import ServiceCl

nginxPath = "/etc/nginx/locations"


class NginxService:

    def updateConfig(self, service: "ServiceCl.ServiceCl", instance: "DockerInstance"):
        locationsPrefix = ""
        if service.internOnly:
            locationsPrefix = "-intern"

        file = f"{nginxPath}{locationsPrefix}/{service.dockerName}.locations"

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
        return self.reload_config(data, file)

    def reload_config(self, previousConfig, file):
        stream = os.popen("service nginx reload")
        output = stream.read()

        if len(output) > 0:
            with open(file, "w") as myfile:
                myfile.write(previousConfig)

            status_str = os.popen("systemctl status nginx.service")
            reset_stream = os.popen("service nginx reload")
            reset_output = reset_stream.read()
            logKibana(LogLevel.ERROR, "nginx didnt start correctly",
                      None, args=dict(status=status_str.read(), reset_out=reset_output))
            return False

        print("reloaded config")
        return True
