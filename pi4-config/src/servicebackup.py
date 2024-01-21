import asyncio
import base64
import os
import re
import time
from typing import Union
import requests
from rsa import aesEncrypt, encryptLargeData
from servicebase import BaseService
from customlogging import LogLevel, logKibana
import json


class BackupService(BaseService):

    def __init__(self, folder_path: str, pattern: str, blackListPattern: Union[str, None] = None):
        super().__init__(folder_path, pattern)
        self.key_path = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                      "..",
                                                      "keys",
                                                      base64.b64encode(self.folder_path.encode()).decode()+".secret"))
        self.key = None
        self.loadKey()
        self.blackListPattern = blackListPattern

    def loadKey(self):
        f = None
        try:
            f = open(self.key_path, "r")
            text = f.read()
            self.key = base64.b64decode(text)
        except IOError as e:
            try:
                os.makedirs(os.path.dirname(self.key_path), exist_ok=True)
                self.key = os.urandom(32)
                f = open(self.key_path, "w")
                f.write(base64.b64encode(self.key).decode())
            except Exception as err:
                print(err)
        finally:
            if f is not None:
                f.close()

    def is_blacklisted(self, path):
        if (self.blackListPattern is not None):
            if (re.match(f".*{self.blackListPattern}.*", path)):
                return True
        return False

    async def triggerChange(self, path: str) -> bool:
        changeTs = int(round(time.time() * 1000))
        await asyncio.sleep(0.5)

        if (self.is_blacklisted(path)):
            logKibana(LogLevel.DEBUG, "blacklisted file backup event", args=dict(
                file=path,
                blacklist_pattern=self.blackListPattern
            ))
            return False

        if (self.key is None):
            raise Exception("key was none ")
        try:
            with open(path, "rb") as file:
                logKibana(LogLevel.INFO, f"backing up file",
                          args=dict(path=path))
                file_content = base64.b64encode(file.read()).decode()
                encrypted_content, iv = aesEncrypt(file_content, self.key)
                encoded_storage_request = encryptLargeData(json.dumps(dict(
                    path=path,
                    content=encrypted_content+"__-__" +
                    base64.b64encode(iv).decode(),
                    timestamp=changeTs
                )))
            target = os.environ.get("BACKUP_TARGET")
            if target is None:
                logKibana(LogLevel.ERROR, f"missing backup target")
                return False
            response = requests.post(
                os.environ["BACKUP_TARGET"], json=dict(data=encoded_storage_request))
            logKibana(LogLevel.INFO, f"backed up file",
                      args=dict(path=path, response=response.text))
            print(response.text)
            return True
        except FileNotFoundError as e:
            print("didnt find " + path)
            # assumed to be a very short lived temporary file
            return False
        except requests.exceptions.ConnectionError:
            logKibana(LogLevel.ERROR, f"failed connecting on backup",
                      args=dict(path=path))
            return False
