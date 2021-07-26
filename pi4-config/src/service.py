from dockerService import healthcheck, run_docker
from nginxService import reloadConfig, setConfig

class Service:

    instances=[]

    def __init__(self,path:str,pattern:str):
        self.folderPath=path
        self.pattern=pattern

    def restart():
        run_docker()
        healthcheck()
        setConfig()
        reloadConfig();
        
