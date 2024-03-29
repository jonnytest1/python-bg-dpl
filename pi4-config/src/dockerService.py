import os
from typing import List

from customlogging import LogLevel, logKibana


def get_all_instances():
    stream = os.popen('docker ps -a')
    lines = stream.readlines()
    return lines[1:]


def get_run_command(containername: str):
    stream = os.popen(
        'docker inspect --format "$(cat ./dockerrun.tpl)" '+containername)
    return stream.read()


def getContainerLogs(containername: str):
    stream = os.popen(
        'docker logs '+containername)
    return stream.read()


def getStatusForContainer(containerName: str):
    stream = os.popen(f'docker ps -a | grep -H {containerName}')
    return stream.read()


def removeContainer(containerName: str):
    stream = os.popen(f'docker stop {containerName}')
    output = stream.read()

    if output.strip() != containerName:
        logKibana(LogLevel.ERROR, "stopping failed", args=dict(output=output))
        raise Exception("stopping failed")

    stream = os.popen(f'docker rm {containerName}')
    output = stream.read().strip()

    if output != containerName:
        logKibana(LogLevel.ERROR, "removing failed", args=dict(output=output))
        raise Exception("removing failed")


def restartContainer(containerName: str, envs: List[str]):
    # docker exec -i CONTAINER_ID /bin/bash -c "export VAR1=VAL1 && export VAR2=VAL2 && your_cmd"

    stream = os.popen(f'docker restart {containerName}')
    output = stream.read().strip()

    if output != containerName:
        logKibana(LogLevel.ERROR, "restarting failed",
                  args=dict(output=output))
        raise Exception("restarting failed")

    return
