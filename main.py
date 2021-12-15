import signature
import AES
import RSA
import os

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
def verifySignature(public_key, signature_data, document_data, directory):
    print("Verifying artist signature")
    hash_artist_file = directory+"artist-hash.txt"
    dec_artist_signature = directory+"dec-artist-signature.txt"
    signature.hashData(document_data, hash_artist_file)
    print(signature_data)
    RSA.decryption(public_key, signature_data, dec_artist_signature)

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
 
    if option == 1:
		#for alice:
        print ("Option 1.")
        name = input("Enter your name: ")
        artwork_file = input("Enter the file name of your artwork: ")
        #password = input("Enter a secret keyword to make the signature: ")
        print(' '+signature.getAuthorMessage(name, artwork_file))
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
            write_file(author_file, signature.getAuthorMessage(name, artwork_file))
            #Hash
            signature.hashDocument(author_file, hash_file)
            #Generating key
            RSA.keyGeneration(pub_file, priv_file)
            #Encryption
            RSA.encryption(priv_file, hash_file, signature_file)
            RSA.decryption(pub_file, readFile(signature_file), directory+'dec.txt')
            join_files(signature_file, author_file, inter_file)
            join_files(inter_file, artwork_file, dist_file)
            print (f"Done! You can find your files in {directory}, share only the dist.txt file")
        else:
            print ("")
        input("Continue?")
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
        #Verify signature
        artist_name = input("Write the artist name: ")
        pub_file = directory+f"{artist_name}-public.pem"
        verified = verifySignature(pub_file, received_signature, received_document, directory)

        #print("Artist signed Document: ")
        #print(received_document)
        #print("Received Artwork: ")
        #print(received_art)

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
