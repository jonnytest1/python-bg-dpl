import os
from rsa import aesEncrypt

key = os.urandom(32)

enc, iv = aesEncrypt("test123", key)


print(enc, iv)
