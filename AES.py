import os
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from base64 import b64decode
from base64 import b64encode
from hashlib import md5
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def encrypt(data, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return b64encode(iv + cipher.encrypt(pad(data.encode('utf-8'),
        AES.block_size)))

def encrypt_file(filename, key, out_file):
    plaintext=''
    with open(filename, 'r') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)
    with open(out_file, 'wb') as fo:
        fo.write(enc)
    return enc

def decrypt(data, key):
    raw = b64decode(data)
    cipher = AES.new(key, AES.MODE_CBC, raw[:AES.block_size])
    return unpad(cipher.decrypt(raw[AES.block_size:]), AES.block_size)

def decrypt_file(filename, key, out_file):
    plaintext=''
    with open(filename, 'r') as fo:
        plaintext = fo.read()
    dec = decrypt(plaintext, key)
    with open(out_file, 'wb') as fo:
        fo.write(dec)
    return dec

def generate_key( filename):
    key = os.urandom(16) #SHA256.new(bytes(password, 'utf-8')).digest()
    with open(filename, 'wb') as fo:
        fo.write(key)