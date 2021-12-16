from datetime import datetime
import AES
import RSA
import os
import sys
from termcolor import colored, cprint
import subprocess
subprocess.call('', shell=True)

def getAuthorMessage(name, filename):
	today= datetime.now()
	message= f"The artwork located in {filename} was made by {name}|{today}|{name}|{filename}"
	return message

def getAgreementMessage(name, artist_name):
	today= datetime.now()
	message= f"Me, {name} agreed to not use this artwork without the consent of its author {artist_name}|{today}|{name}|{artist_name}"
	return message

def getValidationMessage(name, client_name, artist_name):
	today= datetime.now()
	message= f"Me {name} as a public notary validate that the current agreement between the artist {artist_name} and the client {client_name} is valid|{today}|{name}|{client_name}|{artist_name}"
	return message

def askMenuOption():
    validNumber = False
    number = 0
    while(not validNumber):
        try:
            number = int(input("Choose an option: "))
            validNumber = True
        except ValueError:
            print("Error, please enter an int number")   
    return number
def get_directory(filename):
    return os.path.dirname(filename)+"/"
def read_file_bytes(filename):
    with open(filename, 'rb') as fo:
        plaintext = fo.read()
        return plaintext
def write_file(filename, data):
    with open(filename, 'w') as fo:
        fo.write(data)
def readFile(filetext):
    f = open (filetext,'r')
    s = f.read()
    f.close()
    return s
def join_files(file1, file2, out):
    with open(file1) as fp:
        data = fp.read()
    with open(file2) as fp:
        data2 = fp.read()
    data += "@@@"
    data += data2
    with open (out, 'w') as fp:
        fp.write(data)
def generateEncryptKeyPair():
    print ("Option 5.")
    name = input("Enter your name: ")
    directory = input("Enter the directory where you want to save your private key: ")
    print ("Generating key pair")
    private_enc_file = directory+f"/{name}-encrypt-private.pem"
    public_enc_file = f"public/{name}-encrypt-public.pem"
    #Generating key
    RSA.keyGeneration(public_enc_file, private_enc_file)
    print (f"Done! You can find your private key in {directory}")
    input("Continue?")

def signArt():
    name = input("Enter your name: ")
    artwork_file = input("Enter the file name of your artwork: ")
    client_name = input("Enter the name of your client: ")
    print(' '+getAuthorMessage(name, artwork_file))
    res = input("Do you want authorize and sign the previous message (y/n)? ")
    if res=='y':
        print ("Generating digital signature...")
        #Writing author document
        directory=get_directory(artwork_file)
        author_file = directory+"artist-msg.txt"
        hash_file = directory+"artist-hash.txt"
        priv_file = directory+f"{name}-sign-private.pem"
        pub_artist = f"public/{name}-sign-public.pem"
        signature_file = directory+"artist-signature.txt"
        inter_file = directory+"artist-inter.txt"
        data_file = directory+"artist-data.txt"
        aes_key = directory+"artist-aes-key.txt"
        aes_key_enc = directory+"artist-aes-key-enc.txt"
        client_rsa_pub = f"public/{client_name}-encrypt-public.pem"
        enc_file = directory+"artist-data-enc.txt"
        final_file = directory+"artist-dist.txt"
        write_file(author_file, getAuthorMessage(name, artwork_file))
        join_files(author_file, artwork_file, inter_file)
        #Generating key
        RSA.keyGeneration(pub_artist, priv_file)
        #Signature
        RSA.signFile(priv_file, pub_artist, inter_file, signature_file, hash_file)
        join_files(signature_file, inter_file, data_file)
        #generate AES Key
        AES.generate_key(aes_key)
        #encrypt dist file with AES
        AES.encrypt_file(data_file, aes_key, enc_file)
        #encrypt AES Key
        RSA.encryptFile(client_rsa_pub, aes_key, aes_key_enc )
        join_files(aes_key_enc, enc_file, final_file)
        print (f"Done! You can find your files in {directory}, share only the dist.txt file")
        remove = input("Do you want to remove files generated during process (y/n)? ")
        if remove=='y':
            os.remove(aes_key_enc)
            os.remove(author_file)
            os.remove(enc_file)
            os.remove(hash_file)
            os.remove(inter_file)
            os.remove(signature_file)
        else: 
            print ("")
    else:
        print ("")
def signAgreement():
    name = input("Enter your name: ")
    enc_file = input("Enter the file name of the signed file by the artist: ")
    directory=get_directory(enc_file)
    priv_rsa_enc = directory+f"{name}-encrypt-private.pem"
    artist_aes_key = directory+"artist-aes-key.text"
    enc_author_file = directory+"encrypt-artist-msg.text"
    author_file = directory+"artist-msg.text"
    #Decrypt file
    enc_file_data = readFile(enc_file)
    enc_data = enc_file_data.split('@@@')
    enc_aes_key = enc_data[0]
    enc_dist = enc_data[1]
    #decrypt aes key
    RSA.decryptData(priv_rsa_enc, enc_aes_key, artist_aes_key )
    write_file(enc_author_file,enc_dist)
    AES.decrypt_file(enc_author_file,artist_aes_key, author_file)

    #Reading file values
    print("Reading file values...")
    file_data = readFile(author_file)
    data = file_data.split('@@@')
    received_signature = data[0]
    received_document = data[1]
    received_art = data[2]
    data_to_hash = received_document +'@@@'+ received_art
    #Verify signature
    artist_name = input("Write the artist name: ")
    notary_name = input("Write the notary name: ")
    pub_artist = f"public/{artist_name}-sign-public.pem"
    verified = RSA.verifySignature(pub_artist, data_to_hash, received_signature, directory)
    if(verified):
        #Show received data
        cprint('The signature is valid!', 'green')
        print("Check yourself that the received info is correct")
        cprint('Artist signed Document: ', 'magenta')
        print(received_document)
        print('Received Artwork: ', 'magenta')
        print(received_art)
        #Sign agreement
        agreeMsg = getAgreementMessage(name, artist_name)
        print(' '+agreeMsg)
        res = input("Do you want authorize and sign the previous message (y/n)? ")
        if res=='y':
            print ("Generating digital signature")
            #Writing agree document with the previous file appended
            agree_file = directory+"client-msg.txt"
            hash_file = directory+"client-hash.txt"
            priv_file = directory+f"{name}-sign-private.pem"
            pub_client = f"public/{name}-sign-public.pem"
            signature_file = directory+"client-signature.txt"
            inter_file = directory+"client-inter.txt"
            aes_key = directory+"client-aes-key.txt"
            aes_key_enc = directory+"client-aes-key-enc.txt"
            data_file = directory+"client-data.txt"
            data_enc_file = directory+"client-data-enc.txt"
            notary_rsa_pub = f"public/{notary_name}-encrypt-public.pem"
            final_file = directory+"client-dist.txt"
            write_file(agree_file, agreeMsg)
            join_files(agree_file, author_file, inter_file)
            #Generating key
            RSA.keyGeneration(pub_client, priv_file)
            #Sign file
            RSA.signFile(priv_file, pub_client, inter_file, signature_file, hash_file)
            join_files(signature_file, inter_file, data_file)

            #generate AES Key
            AES.generate_key(aes_key)
            #encrypt dist file with AES
            AES.encrypt_file(data_file, aes_key, data_enc_file)
            #encrypt AES Key
            RSA.encryptFile(notary_rsa_pub, aes_key, aes_key_enc )
            join_files(aes_key_enc, enc_file, final_file)

            print (f"Done! You can find your files in {directory}, share only the artist-client-agreement.txt file")
        else:
            print ("")
        remove = input("Do you want to remove files generated during process (y/n)? ")
        if remove=='y':
            os.remove(enc_author_file)
            os.remove(agree_file)
            os.remove(hash_file)
            os.remove(inter_file)
            os.remove(signature_file)
            os.remove(aes_key_enc)
            os.remove(data_enc_file)
        else: 
            print ("")
    else:
        print("The signature is not valid!!")
def verifyBothSignatures():
    name = input("Enter your name: ")
    agreement_file = input("Enter the file name of the agreement artist-client: ")
    directory=get_directory(agreement_file)
    #Reading file values
    print("Reading file values")
    file_data = readFile(agreement_file)
    data = file_data.split('@@@')
    client_signature = data[0]
    client_agreement = data[1]
    artist_signature = data[2]
    artist_author = data[3]
    received_art = data[4]
    data_to_hash_artist = artist_author +'@@@'+ received_art
    data_to_hash_client = client_agreement +'@@@'+ artist_signature+'@@@'+ data_to_hash_artist
    #Verify signature
    artist_name = input("Write the artist name: ")
    client_name = input("Write the client name: ")
    pub_artist = f"public/{artist_name}-public.pem"
    pub_client = f"public/{client_name}-public.pem"
    verified_artist = RSA.verifySignature(pub_artist, data_to_hash_artist, artist_signature, directory)
    verified_client = RSA.verifySignature(pub_client, data_to_hash_client, client_signature, directory)
    if( verified_artist and verified_client ):
        #Show received data
        print("Both signatures are valid!")
        print("Check yourself that the received info is correct")
        print("Artist signed Document: ")
        print(artist_author)
        print("Received Artwork: ")
        print(received_art)
        print("Client signed Document: ")
        print(client_agreement)
        #Sign validation
        validateMsg = getValidationMessage(name, client_name, artist_name)
        print(' '+validateMsg)
        res = input("Do you want to validate the information and sign it (y/n)? ")
        if res=='y':
            print ("Generating digital signature")
            #Writing validate document with the previous file appended
            validate_file = directory+"validate.txt"
            hash_file = directory+"hash.txt"
            priv_notary = directory+f"{name}-private.pem"
            pub_notary = f"public/{name}-public.pem"
            signature_file = directory+"signature.txt"
            inter_file = directory+"inter.txt"
            final_file = directory+"validated-document.txt"
            write_file(validate_file, validateMsg)
            join_files(validate_file, agreement_file, inter_file)
            #Generating key
            RSA.keyGeneration(pub_notary, priv_notary)
            #Sign file
            RSA.signFile(priv_notary, pub_notary, inter_file, signature_file, hash_file)
            join_files(signature_file, inter_file, final_file)
            print (f"Done! You can find your files in {directory}, share only the validated-document.txt file")
        else:
            print ("")
    else:
        print("The signatures are not valid!!")
def verifyNotaryDocument():
    final_file = input("Enter the file name of the notary document: ")
    directory=get_directory(final_file)
    #Reading file values
    print("Reading file values")
    file_data = readFile(final_file)
    data = file_data.split('@@@')
    notary_signature = data[0]
    notary_validation = data[1]
    client_signature = data[2]
    client_agreement = data[3]
    artist_signature = data[4]
    artist_author = data[5]
    received_art = data[6]
    data_to_hash_artist = artist_author +'@@@'+ received_art
    data_to_hash_client = client_agreement +'@@@'+ artist_signature+'@@@'+ data_to_hash_artist
    data_to_hash_notary = notary_validation +'@@@'+ client_signature+'@@@'+ data_to_hash_client
    #Verify signature
    actors_data = notary_validation.split('|')
    notary_name = actors_data[2]#input("Write the notary name: ")
    client_name = actors_data[3]#input("Write the client name: ")
    artist_name = actors_data[4]#input("Write the artist name: ")
    #geting public keys
    pub_notary = f"public/{notary_name}-public.pem"
    pub_artist = f"public/{artist_name}-public.pem"
    pub_client = f"public/{client_name}-public.pem"
    verified_notary = RSA.verifySignature(pub_notary, data_to_hash_notary, notary_signature, directory)
    verified_artist = RSA.verifySignature(pub_artist, data_to_hash_artist, artist_signature, directory)
    verified_client = RSA.verifySignature(pub_client, data_to_hash_client, client_signature, directory)
    if( verified_notary and verified_artist and verified_client ):
        #Show received data
        print("All the signatures are VALID!")
        print("Check yourself that the received info is correct")
        print("Artwork: ")
        print(received_art)
        print("Artist signed Document: ")
        print(artist_author)
        print("Client signed Document: ")
        print(client_agreement)
        print("Notary signed Document: ")
        print(notary_validation)
    else:
        print("The signatures are not valid!!")


directory=''
exit = False
option = 0
while not exit:  
    print("****************************************") 
    cprint('PROTECTING DIGITAL ART\n', 'green', 'on_blue')
    cprint('Cipriano Damián Sebastián', 'green', 'on_blue')
    cprint('Palacios Lugo Alan Yoltic', 'green', 'on_blue')
    cprint('Tovar Espejo Mariana Josefina', 'green', 'on_blue')
    print("****************************************")  
    print ("Choose what you want to do")  
    print ("1. Sign your art")
    print ("2. Sign agreement not to use without the consent of the artist")
    print ("3. Verify both signs")
    print ("4. View notary document")
    print ("5. Generate encryption key pair")
    print ("6. Exit")

    option = askMenuOption()
    if option == 1:
        cprint ('Option 1.', 'blue')
        signArt()
        input("Continue?")
    elif option == 2:
        cprint ('Option 2','blue')
        signAgreement()
        input("Continue?")
    elif option == 3:
        print("Option 3")
        verifyBothSignatures()
        input("Continue?")
    elif option == 4:
        print("Option 4")
        verifyNotaryDocument()
        input("Continue?")
    elif option == 5:
        print("Option 4")
        generateEncryptKeyPair()
        input("Continue?")
    elif option == 6:
        exit = True
    else:
        print ("Choose a number among 1 and 5")
print ("Bye")

