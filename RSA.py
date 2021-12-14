from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def keyGeneration(public_file, private_file):
    #Generar pareja de claves RSA de 2048 bits de longitud
    key = RSA.generate(2048)

    #Private key
    private_key = key.export_key()

    #Save the private key in a .pem file
    with open(public_file, "wb") as f:
        f.write(private_key)

    #Obtain the public key
    public_key = key.publickey().export_key()

    #Save the public key in a .pem file
    with open(private_file, "wb") as f:
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

#file_text=input("Nombre del archivo: ")
#file_text2=input("Nombre del archivo para texto cifrado: ")
#file_text3=input("Nombre del archivo para texto descifrado: ")
#
#priv = "private.pem"
#pub = "public.pem"
#
#s = readDoc(file_text)
#keyGeneration()
#cip_text = encryption(priv, s)
#saveDoc(file_text2,cip_text)
#s2 = readDoc2(file_text2)
#dec_text = decryption(pub,s2)
#saveDoc2(file_text3,dec_text)