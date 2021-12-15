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
            pub_file = directory+f"{name}-public.pem"
            signature_file = directory+"signature.txt"
            inter_file = directory+"inter.txt"
            dist_file = directory+"dist.txt"
            write_file(author_file, getAuthorMessage(name, artwork_file))
            join_files(author_file, artwork_file, inter_file)
            #Generating key
            RSA.keyGeneration(pub_file, priv_file)
            #Encryption
            RSA.signFile(priv_file, pub_file, inter_file, signature_file, hash_file)
            join_files(signature_file, inter_file, dist_file)
            print (f"Done! You can find your files in {directory}, share only the dist.txt file")
        else:
            print ("")
        input("Continue?")

	#verify signed document:
    elif option == 2:
		#for bob:
		#verify and show document received by alice
		#sign document of not use without authorization previosly requesting the name
		#verify final document received by notary
		#show final document
        print ("Option 2")
        name = input("Enter your name: ")
        artist_signed_file = input("Enter the file name of the signed file by the artist: ")
        directory=get_directory(artist_signed_file)
        #Reading file values
        print("Reading file values")
        file_data = readFile(artist_signed_file)
        data = file_data.split('@@@')
        received_signature = data[0]
        received_document = data[1]
        received_art = data[2]
        data_to_hash = received_document +'@@@'+ received_art
        #Verify signature
        artist_name = input("Write the artist name: ")
        pub_file = directory+f"{artist_name}-public.pem"
        verified = RSA.verifySignature(pub_file, data_to_hash, received_signature, directory)
        if(verified):
            print("The signature is valid!!")
            print("Artist signed Document: ")
            print(received_document)
            print("Received Artwork: ")
            print(received_art)

            #print(' '+signature.getAgreementMessage(name, artist_name))
            #res = input("Do you want authorize and sign the previous message (y/n)? ")
            #if res=='y':
            #    print ("Generating digital signature")
            #    #Writing author document
            #    agreement_file = directory+"agree.txt"

            #    hash_file = directory+"hash.txt"
            #    priv_file = directory+f"{name}-private.pem"
            #    signature_file = directory+"signature.txt"
            #    inter_file = directory+"inter.txt"
            #    dist_file = directory+"dist.txt"
            #    write_file(author_file, signature.getAuthorMessage(name, artwork_file))
            #    #Hash
            #    signature.hashDocument(author_file, hash_file)
            #    #Generating key
            #    RSA.keyGeneration(pub_file, priv_file)
            #    #Encryption
            #    RSA.encryption(priv_file, hash_file, signature_file)
            #    join_files(signature_file, author_file, inter_file)
            #    join_files(inter_file, artwork_file, dist_file)
            #    print (f"Done! You can find your files in {directory}, share only the dist.txt file")
            #else:
            #    print ("")
            #author_file = directory+"author.txt"
        else:
            print("The signature is not valid!!")
        input("Continue?")
    elif option == 3:
        print("Option 3")
        input("Continue?")
		#for notary:
		#verify and show document received by bob and alice
		#sign document of validation if the notary decide it 
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
