import os


def get_all_instances():
    stream = os.popen('docker ps -a')
    lines = stream.readlines()
    return lines[1:]


def getRunCommand(containername: str):
    stream = os.popen(
        'docker inspect --format "$(cat ./dockerrun.tpl)" '+containername)
    return stream.read()


def getStatusForContainer(containerName: str):
    stream = os.popen(f'docker ps -a | grep -H {containerName}')
    return stream.read()
