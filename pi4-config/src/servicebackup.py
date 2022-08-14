import asyncio
import base64
from datetime import datetime
import os
import time
from winreg import LoadKey
import requests
from rsa import aesEncrypt, encryptLargeData
from servicebase import BaseService
from customlogging import LogLevel, logKibana
import json


class BackupService(BaseService):

    def __init__(self, folder_path: str, pattern: str):
        super().__init__(folder_path, pattern)
        self.key_path = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                      "..",
                                                      "keys",
                                                      base64.b64encode(self.folder_path.encode()).decode()+".secret"))
        self.key = None
        self.loadKey()

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

    async def triggerChange(self, path: str) -> bool:
        logKibana(LogLevel.INFO, f"backing up file", args=dict(path=path))
        changeTs = int(round(time.time() * 1000))
        await asyncio.sleep(0.5)

        if (self.key is None):
            raise Exception("key was none ")

        with open(path, "rb") as file:
            file_content = file.read().decode("ascii")
            encrypted_content, iv = aesEncrypt(file_content, self.key)
            encoded_storage_request = encryptLargeData(json.dumps(dict(
                path=path,
                content=encrypted_content+"__-__" +
                base64.b64encode(iv).decode(),
                timestamp=changeTs
            )))

        response = requests.post(
            "http://localhost:61234/data", json=dict(data=encoded_storage_request))

        print(response.text)
        return True
