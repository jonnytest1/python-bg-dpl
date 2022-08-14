import json
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, hashes
import base64
import os


def encryptWithPublicKey(data: str):
    with open("D:\\Jonathan\\Projects\\node\\backup\\certs\\7ac704ad-8c42-478d-b9e6-c0024f41abac\\public.pem", "rb") as pub:

        pubKey = serialization.load_pem_public_key(pub.read())
        if (isinstance(pubKey, rsa.RSAPublicKey)):
            # RSA/ECB/OAEPWithSHA-256AndMGF1Padding
            encrypted = pubKey.encrypt(str.encode(data),
                                       padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA256(),
                label=None
            ))
            base64_bytes = base64.b64encode(encrypted).decode("ascii")
            print(base64_bytes)
            return base64_bytes


def aesEncrypt(data: str, key: bytes):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(str.encode(data))+encryptor.finalize()
    return base64.b64encode(ct).decode(), iv


def encryptLargeData(large_data: str):

    key = os.urandom(32)
    data, iv = aesEncrypt(large_data, key)

    return json.dumps(dict(
        aes_data=data,
        aes_credentials=encryptWithPublicKey(json.dumps(dict(
            iv=base64.b64encode(iv).decode(),
            key=base64.b64encode(key).decode()
        )))
    ))
