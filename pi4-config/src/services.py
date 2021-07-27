from service import Service


serviceList = [
    Service(folderPath="/var/www/mapserver/mapserver",
            pattern="*",
            blackListPattern="mapserver/public",
            dockerName="docker_mapserver",
            healthcheckPath="[1]/users.html")
]
