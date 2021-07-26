import os
import re

def get_run_command(imageName:str):
    stream= os.popen('docker inspect --format "$(cat ./dockerrun.tpl)" '+imageName)
    output=stream.read()
    return output

def run_docker(image:str,volumePath):
    command=get_run_command(image)
    command=re.sub(r'--publish "0.0.0.0:([0-9]*):([0-9]*)/t',r'+-publish "0.0.0.0:20000-30000:\g<2>/t',command)
    command.replace()

    stream= os.popen('docker run -d '+image)
    output=stream.read()

    """    
    \
    --name hello-BLUE \
    -v $(pwd)/hello.py:/usr/local/src/hello.py \
    --net=example \
     \
    python:3 \
    python /usr/local/src/hello.py 



    -p 20000-30000


    then read from stats
    """
    print("running")


def healthcheck():
    print("health")


def kill_docker():
    print("kill contianer")
