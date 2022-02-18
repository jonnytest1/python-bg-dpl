from datetime import datetime, timezone
from enum import Enum
import requests
import json
import traceback
import base64
from threading import Thread
import time


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"
    WARNING = "WARNING"


logcounter = 0
epoch = datetime.utcfromtimestamp(0)


def doBackupRequest(x: dict):
    time.sleep(10)
    doRequest(x)


def doRequest(x: dict):
    try:
        jsonstr = json.dumps(x)
        encoded = base64.b64encode(jsonstr.encode("utf-8")).decode("utf-8")
        response = requests.post(
            "https://pi4.e6azumuvyiabvs9s.myfritz.net/tm/libs/log/index.php", data=encoded)

        if(response.status_code == 502):
            bT = Thread(target=doBackupRequest, args=[x])
            bT.start()
    except requests.exceptions.ConnectionError:
        bT = Thread(target=doBackupRequest, args=[x])
        bT.start()


def logKibana(level: LogLevel, msg: str, e: Exception = None, args=dict()):
    global logcounter
    logcounter += 1
    print(msg)
    x = {
        "application": "python filewatcher",
        "Severity": level.name,
        "message": msg,
        "logStack": "".join(traceback.extract_stack().format())
    }
    for key in args:
        if args[key] and isinstance(args[key], datetime):
            val: datetime = args[key]
            args[key] = val.replace(microsecond=0).astimezone().isoformat()
    x.update(args)
    x['count'] = logcounter
    if e != None:
        if not (isinstance(e, Exception)):
            x.update(e)
        else:
            x["error_message"] = ''.join(e.args)
            x["error_stacktrace"] = ''.join(traceback.format_exception(
                etype=type(e), value=e, tb=e.__traceback__))
    t = Thread(target=doRequest, args=[x])
    try:
        t.start()
    except RuntimeError as e:
        print("error while logging")
        time.sleep(1)
        return logKibana(level, msg, e, args)
