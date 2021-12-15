from datetime import datetime
import AES
import RSA
import os

def getAuthorMessage(name, filename):
	today= datetime.now()
	message= f"The artwork located in {filename} was made by {name} - {today}|{name}|{filename}"
	return message

def getAgreementMessage(name, artist_name):
	today= datetime.now()
	message= f"Me, {name} agreed to not use this artwork without the consent of its author {artist_name} - {today}|{name}|{artist_name}"
	return message

def getValidationMessage(name, client_name, artist_name):
	today= datetime.now()
	message= f"Me {name} as a public notary validate that the current agreement between the artist {artist_name} and the client {client_name} is valid - {today}|{name}|{client_name}|{artist_name}"
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

#key = b'123456789012345678901234'
directory=''
exit = False
option = 0
while not exit:  
    print("****************************************")  
    print("Choose what you want to do")  
    print ("1. Sign your art")
    print ("2. Sign agreement not to use without the consent of the artist")
    print ("3. Verify both signs")
    print ("4. View notary document")
    print ("5. Exit")

    option = askMenuOption()
	#sign art:
    if option == 1:
        print ("Option 1.")
        name = input("Enter your name: ")
        artwork_file = input("Enter the file name of your artwork: ")
        #password = input("Enter a secret keyword to make the signature: ")
        print(' '+getAuthorMessage(name, artwork_file))
        res = input("Do you want authorize and sign the previous message (y/n)? ")
        if res=='y':
            print ("Generating digital signature")
            #Writing author document
            directory=get_directory(artwork_file)
            author_file = directory+"author.txt"
            hash_file = directory+"hash.txt"
            priv_file = directory+f"{name}-private.pem"
            pub_artist = f"public/{name}-public.pem"
            signature_file = directory+"signature.txt"
            inter_file = directory+"inter.txt"
            final_file = directory+"dist.txt"
            write_file(author_file, getAuthorMessage(name, artwork_file))
            join_files(author_file, artwork_file, inter_file)
            #Generating key
            RSA.keyGeneration(pub_artist, priv_file)
            #Encryption
            RSA.signFile(priv_file, pub_artist, inter_file, signature_file, hash_file)
            join_files(signature_file, inter_file, final_file)
            print (f"Done! You can find your files in {directory}, share only the dist.txt file")
        else:
            print ("")
        input("Continue?")
	#verify signed document:
    elif option == 2:
		#for bob:
		#verify final document received by notary
		#show final document
        print ("Option 2")
        name = input("Enter your name: ")
        author_file = input("Enter the file name of the signed file by the artist: ")
        directory=get_directory(author_file)
        #Reading file values
        print("Reading file values")
        file_data = readFile(author_file)
        data = file_data.split('@@@')
        received_signature = data[0]
        received_document = data[1]
        received_art = data[2]
        data_to_hash = received_document +'@@@'+ received_art
        #Verify signature
        artist_name = input("Write the artist name: ")
        pub_artist = f"public/{artist_name}-public.pem"
        verified = RSA.verifySignature(pub_artist, data_to_hash, received_signature, directory)
        if(verified):
            #Show received data
            print("The signature is valid!")
            print("Check yourself that the received info is correct")
            print("Artist signed Document: ")
            print(received_document)
            print("Received Artwork: ")
            print(received_art)
            #Sign agreement
            agreeMsg = getAgreementMessage(name, artist_name)
            print(' '+agreeMsg)
            res = input("Do you want authorize and sign the previous message (y/n)? ")
            if res=='y':
                print ("Generating digital signature")
                #Writing agree document with the previous file appended
                agree_file = directory+"agree.txt"
                hash_file = directory+"hash.txt"
                priv_file = directory+f"{name}-private.pem"
                pub_client = f"public/{name}-public.pem"
                signature_file = directory+"signature.txt"
                inter_file = directory+"inter.txt"
                final_file = directory+"artist-client-agreement.txt"
                write_file(agree_file, agreeMsg)
                join_files(agree_file, author_file, inter_file)
                #Generating key
                RSA.keyGeneration(pub_client, priv_file)
                #Sign file
                RSA.signFile(priv_file, pub_client, inter_file, signature_file, hash_file)
                join_files(signature_file, inter_file, final_file)
                print (f"Done! You can find your files in {directory}, share only the artist-client-agreement.txt file")
            else:
                print ("")
        else:
            print("The signature is not valid!!")
        input("Continue?")
    elif option == 3:
		#for notary:
		#verify and show document received by bob and alice
		#sign document of validation if the notary decide it 
        print("Option 3")
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
        input("Continue?")
    elif option == 4:
		#verify final document received by notary
		#show final document
        print("Option 3")
        input("Continue?")
    elif option == 5:
        exit = True
    else:
        print ("Choose a number among 1 and 5")
print ("Bye")
