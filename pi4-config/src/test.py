import re
from customlogging import LogLevel, logKibana

from dockerInstance import DockerInstance

from services import serviceList
data = '--publish "0.0.0.0:15748:4747/tcp" \\   --publish "0.0.0.0:15748:4747/tcp" \\'

repl = re.sub(r'--publish "0.0.0.0:([0-9]*):([0-9]*)/t',
              r'+-publish "0.0.0.0:20000-30000:\g<2>/t', data)

print(repl)


instance = DockerInstance(
    "d33455c698f3        jonathanheindl/rpi-nodets          \"/bin/sh -c /node.sh\"    2 months ago        Up 11 hours         0.0.0.0:15748->4747/tcp, 0.0.0.0:17935->8080/tcp                           docker_mapserver_1")
print(instance.image)
print(instance.name)


changed = serviceList[0].triggerChange(
    "/var/www/mapserver/mapserver/public/nue-script.js")
print(f"changed {changed}")


serviceList[0].getEnvForPath(
    "/var/www/mapserver/mapserver/public/nue-script.js")


env=serviceList[0].getEnvForPath(
    "/var/www/mapserver/mapserver/package.json")


#logKibana(LogLevel.ERROR, "test")


command = ''' docker run \
  --name "/docker_mapserver_2" \
  --runtime "runc" \
  --volume "/var/www/mapserver/mapserver:/var/node" \
  --volume "546cfdc53024f9a181b9b488f41abc26cb3289c3f797a0cb3ca017c78d35f6cb:/var/node/node_modules" \
  --log-driver "json-file" \
  --restart "unless-stopped" \
  --cap-add "AUDIT_WRITE" \
  --cap-add "CHOWN" \
  --cap-add "DAC_OVERRIDE" \
  --cap-add "FOWNER" \
  --cap-add "FSETID" \
  --cap-add "KILL" \
  --cap-add "MKNOD" \
  --cap-add "NET_BIND_SERVICE" \
  --cap-add "NET_RAW" \
  --cap-add "SETFCAP" \
  --cap-add "SETGID" \
  --cap-add "SETPCAP" \
  --cap-add "SETUID" \
  --cap-add "SYS_CHROOT" \
  --cap-drop "AUDIT_CONTROL" \
  --cap-drop "BLOCK_SUSPEND" \
  --cap-drop "DAC_READ_SEARCH" \
  --cap-drop "IPC_LOCK" \
  --cap-drop "IPC_OWNER" \
  --cap-drop "LEASE" \
  --cap-drop "LINUX_IMMUTABLE" \
  --cap-drop "MAC_ADMIN" \
  --cap-drop "MAC_OVERRIDE" \
  --cap-drop "NET_ADMIN" \
  --cap-drop "NET_BROADCAST" \
  --cap-drop "SYSLOG" \
  --cap-drop "SYS_ADMIN" \
  --cap-drop "SYS_BOOT" \
  --cap-drop "SYS_MODULE" \
  --cap-drop "SYS_NICE" \
  --cap-drop "SYS_PACCT" \
  --cap-drop "SYS_PTRACE" \
  --cap-drop "SYS_RAWIO" \
  --cap-drop "SYS_RESOURCE" \
  --cap-drop "SYS_TIME" \
  --cap-drop "SYS_TTY_CONFIG" \
  --cap-drop "WAKE_ALARM" \
  --publish "0.0.0.0:20000-30000:4747/tcp" \
  --publish "0.0.0.0:20000-30000:8080/tcp" \
  --network "docker_host" \
  --network-alias "1775fa34fa54" \
  --hostname "d33455c698f3" \
  --expose "4747/tcp" \
  --expose "8080/tcp" \
  --env "DB_URL=docker_maria_1" \
  --env "LC_ALL=C.UTF-8" \
  --env "QEMU_CPU=arm1176" \
  --env "DB_PASSWORD=work123adventur3" \
  --env "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
  --env "SKIP_NPM=TRUE" \
  --env "DB_USER=workadventure" \
  --env "DEBIAN_FRONTEND=noninteractive" \
  --env "UDEV=off" \
  --env "affinity:container==bb7ea4cdd1d169a78e2b63d0ed1c61f8b664c81ab76a3a107a0e1e3f0e201afa" \
  --env "DB_PORT=3306" \
  --env "ADMIN_API_KEY=123" \
  --env "DB_NAME=worldmap" \
  --label "com.docker.compose.config-hash"="cbf63456f7bc0a9a09bbb41b0df28dd66ad747aa7d962dabab36cd101e8eba2e" \
  --label "com.docker.compose.container-number"="1" \
  --label "com.docker.compose.oneoff"="False" \
  --label "com.docker.compose.project"="docker" \
  --label "com.docker.compose.service"="mapserver" \
  --label "com.docker.compose.version"="1.24.1" \
  --label "io.balena.architecture"="rpi" \
  --label "io.balena.device-type"="raspberrypi" \
  --label "io.balena.qemu.version"="" \
  --detach \
  --tty \
  --interactive \
  "jonathanheindl/rpi-nodets:latest" \
 '''

for key, value in dict(SKIP_NPM=False).items():
    if value == True:
        print(f"adding {key}")
        command = command.replace(
            "--env", f"--env \"{key}=TRUE\" \\\n\t--env", 1)
    else:
        print(f"removin {key}")
        command = command.replace(f"--env \"{key}=TRUE\"", "")

print(command)
