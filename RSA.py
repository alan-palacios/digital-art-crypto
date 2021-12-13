from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def keyGeneration():
    #Generar pareja de claves RSA de 2048 bits de longitud
    key = RSA.generate(2048)

    #Encrypt the private key
    secret_code = "12345"
    private_key = key.export_key(passphrase=secret_code)

    #Save the private key in a .pem file
    with open("private.pem", "wb") as f:
        f.write(private_key)

    #Obtain the public key
    public_key = key.publickey().export_key()

    #Save the public key in a .pem file
    with open("public.pem", "wb") as f:
        f.write(public_key)

def encryption():
    #Example of string to encrypt
    s = "Pongame 10"

    #Convert the string into bytes
    byteData = s.encode("utf-8")

    #Read the file with the public key
    with open("public.pem", "rb") as f:
        recipient_key = f.read()
    key = RSA.importKey(recipient_key)

    #Instance of the cipher
    cipher_rsa = PKCS1_OAEP.new(key)

    #Encrypt the string using the public key
    encData = cipher_rsa.encrypt(byteData)

    return encData

def decryption(encData):
    #Read the file with the public key
    with open("private.pem", "rb") as f:
        recipient_key = f.read()
    key = RSA.importKey(recipient_key, passphrase="12345")
    
    #Instance of the cipher
    cipher_rsa = PKCS1_OAEP.new(key)

    #Decrypt the string using the private key
    decData = cipher_rsa.decrypt(encData)

    #Convert the byte string to characters
    s = decData.decode("utf-8")

    return s