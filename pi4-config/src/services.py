from ServiceCl import ServiceCl


serviceList = [
    ServiceCl(folderPath="/var/www/mapserver/mapserver",
              pattern="*",
              blackListPattern="mapserver/public",
              dockerName="docker_mapserver",
              healthcheckPath="[1]/users.html",
              envDictionary=dict(SKIP_NPM="^(?!(.*)package\.json).*$"))
]
