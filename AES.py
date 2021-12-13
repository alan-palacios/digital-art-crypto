from Crypto.Cipher import AES
from base64 import b64decode
from base64 import b64encode
from hashlib import md5
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def encrypt(key, data):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return b64encode(iv + cipher.encrypt(pad(data.encode('utf-8'),
        AES.block_size)))

def decrypt(key, data):
    raw = b64decode(data)
    cipher = AES.new(key, AES.MODE_CBC, raw[:AES.block_size])
    return unpad(cipher.decrypt(raw[AES.block_size:]), AES.block_size)