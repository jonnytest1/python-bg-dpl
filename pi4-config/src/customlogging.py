from typing import Union
from datetime import datetime
from enum import Enum
import requests
import json
import traceback
import base64
from threading import Thread
import time
import os


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
        logging_endpoint = os.environ.get(
            "LOGGING_ENDPOINT")
        if (logging_endpoint is None):
            print("missing log endpoint")
            return
        response = requests.post(logging_endpoint, data=encoded)

        if (response.status_code == 502):
            bT = Thread(target=doBackupRequest, args=[
                        x], name="logbackupthread")
            bT.start()
    except requests.exceptions.ConnectionError:
        bT = Thread(target=doBackupRequest, args=[
                    x], name="logbackupthreadconerror")
        bT.start()


def logKibana(level: LogLevel, msg: str, e: Union[Exception, None] = None, args=dict()):
    global logcounter
    logcounter += 1
    print(msg)
    x: dict[str, Union[str, int]] = {
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
        p_exception = e
        if not (isinstance(e, Exception)):
            x.update(e)
        else:
            x["error_stacktrace"] = ''.join(traceback.format_exception(
                etype=type(e), value=e, tb=e.__traceback__))
            try:
                x["error_message"] = ''.join(p_exception.args)
            except Exception:
                for i in range(len(p_exception.args)):
                    x["error_arg"+str(i)] = str(p_exception.args[i])

    t = Thread(target=doRequest, args=[x], name="logthread")
    try:
        t.start()
    except RuntimeError as e:
        print("error while logging")
        time.sleep(1)
        return logKibana(level, msg, e, args)
