from base64 import b64encode
from Crypto.Hash import SHA256
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
import base64

def keyGeneration(public_file, private_file):
    #Generar pareja de claves RSA de 2048 bits de longitud
    key = RSA.generate(2048)

    #Private key
    private_key = key.export_key()

    #Save the private key in a .pem file
    with open(private_file, "wb") as f:
        f.write(private_key)

    #Obtain the public key
    public_key = key.publickey().export_key()

    #Save the public key in a .pem file
    with open(public_file, "wb") as f:
        f.write(public_key)

def encryption(priv_file, data, out):
    #Convert the string into bytes
    byteData = data.encode("ascii")

    #Read the file with the public key
    with open(priv_file, "rb") as f:
        recipient_key = f.read()
    key = RSA.importKey(recipient_key)

    #Instance of the cipher
    cipher_rsa = PKCS1_OAEP.new(key)

    #Encrypt the string using the public key
    encData = cipher_rsa.encrypt(byteData)

    #Write file
    f = open (out,'wb')
    f.write(base64.b64encode(encData))
    f.close()

def decryption(pub_file, encData, out):
    #Read the file with the public key
    with open(pub_file, "rb") as f:
        recipient_key = f.read()
    key = RSA.importKey(recipient_key)
    
    #Instance of the cipher
    cipher_rsa = PKCS1_OAEP.new(key)

    #Decrypt the string using the private key
    decData = cipher_rsa.decrypt(encData)

    #Convert the byte string to characters
    s = decData.decode("ascii")

    #write file
    f = open (out,'w')
    f.write(s)
    f.close()

def readDoc(filetext):
    f = open (filetext,'r')
    s = f.read()
    f.close()
    return s

def readDoc2(filetext):
    f = open (filetext,'rb')
    s = f.read()
    f.close()
    s = base64.b64decode(s)
    return s

def saveDoc(filetext,text):
    f = open (filetext,'wb')
    f.write(base64.b64encode(text))
    f.close()

def saveDoc2(filetext,text):
    f = open (filetext,'w')
    f.write(text)
    f.close()
def signFile(priv_file, data, out):
    with open(priv_file, 'r') as f:
        private_key = RSA.import_key(f.read())
    digest = SHA256.new(data)
    signature = pkcs1_15.new(private_key).sign(digest)
    saveDoc2('digest.txt', digest)
    print(signature)
    return signature
def verifyFile(pub_file, digest, signature, out):
    with open(pub_file, 'r') as f:
        public_key = RSA.import_key(f.read())
    verification = pkcs1_15.new(public_key).verify(digest, signature)
    print(verification)

keyGeneration('public.pem','private.pem')
# create a message
message = 'hello'
# load private key
with open('private.pem', 'r') as f:
    private_key = RSA.import_key(f.read())
# hash the message
digest = SHA256.new(message.encode('utf8'))
# sign the digest
signature = pkcs1_15.new(private_key).sign(digest)
# load public key
with open('public.pem', 'r') as f:
    public_key = RSA.import_key(f.read())
# verify the digest and signature
verified = pkcs1_15.new(public_key).verify(digest, signature)
# base64 encode the signature
signature_b64 = b64encode(signature)
print(signature_b64)