from base64 import b64decode, b64encode
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

def signData(priv_file, public_file, hash_data, out_sign, out_hash):
    # load private key
    with open(priv_file, 'r') as f:
        private_key = RSA.import_key(f.read())
    # sign the digest
    digest = SHA256.new(hash_data.encode('utf8'))
    with open(out_hash, 'wb') as fo:
        fo.write(b64encode(digest.digest()))

    signature = pkcs1_15.new(private_key).sign(digest)
    # load public key
    with open(public_file, 'r') as f:
        public_key = RSA.import_key(f.read())
    # verify the digest and signature
    pkcs1_15.new(public_key).verify(digest, signature)
    # base64 encode the signature
    signature_b64 = b64encode(signature)
    #Write file
    f = open (out_sign,'wb')
    f.write(signature_b64)
    f.close()
    
def signFile(priv_file, public_file, hash_file, out_sign, out_hash):
    with open(hash_file, "r") as f:
        hash_data = f.read()
    signData(priv_file, public_file, hash_data, out_sign, out_hash)

def verifySignature(pub_file, hash_data, signature, directory):
    # load public key
    with open(pub_file, 'r') as f:
        public_key = RSA.import_key(f.read())
    # sign the digest
    digest = SHA256.new(hash_data.encode('utf8'))
    #out_hash=directory+"artist-hash.txt"
    #with open(out_hash, 'wb') as fo:
    #    fo.write(b64encode(digest.digest()))
    # verify the digest and signature
    signature = b64decode(signature)
    try:
        pkcs1_15.new(public_key).verify(digest, signature)
        return True
    except:
        return False

def decryptFile(priv_file, data_file, out):
    #Read the file with the public key
    with open(data_file, "rb") as f:
        encData = f.read()
    #Read the file with the public key
    with open(priv_file, "rb") as f:
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

def encryptFile(pub_file, data_file, out):
    #Read the file with the public key
    with open(data_file, "rb") as f:
        byteData = f.read()
    #Convert the string into bytes
    #byteData = data.encode("ascii")

    #Read the file with the public key
    with open(pub_file, "rb") as f:
        recipient_key = f.read()
    key = RSA.importKey(recipient_key)

    #Instance of the cipher
    cipher_rsa = PKCS1_OAEP.new(key)

    #Encrypt the string using the public key
    encData = cipher_rsa.encrypt(byteData)

    #Write file
    f = open (out,'wb')
    f.write(b64encode(encData))
    f.close()