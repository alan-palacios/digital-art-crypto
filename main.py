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
    print ("4. Exit")

    option = askMenuOption()
 
    if option == 1:
        print ("Option 1.")
        name = input("Enter your name: ")
        artwork_file = input("Enter the file name of your artwork: ")
        password = input("Enter a secret keyword to make the signature: ")
        print(' '+signature.getAuthorMessage(name, artwork_file))
        res = input("Do you want authorize and sign the previous message (y/n)? ")
        if res=='y':
            print ("Generating digital signature")
            #Writing author document
            directory=get_directory(artwork_file)
            author_file = directory+"author.txt"
            write_file(author_file, signature.getAuthorMessage(name, artwork_file))
            #Hash
            signature.hashDocument(author_file)
            #Generating key
            key_file = directory+"key.aes"
            AES.generate_key(password, key_file)
            key=read_file_bytes(key_file)
            #Encrypt
            AES.encrypt_file(author_file+'.hash', key)
            AES.decrypt_file(author_file+'.hash.aesenc', key)
            print (f"Done! You can find your files in {directory}")
        else:
            print ("")
        input("Continue?")
		#for alice:
		#sign artwork previously requesting the name of the artist and showing the message of ownership that will be added:
		#verify final document received by notary
		#show final document
    elif option == 2:
        print ("Option 2")
        input("Continue?")
		#for bob:
		#verify and show document received by alice
		#sign document of not use without authorization previosly requesting the name
		#verify final document received by notary
		#show final document
    elif option == 3:
        print("Option 3")
        input("Continue?")
		#for notary:
		#verify and show document received by bob and alice
		#sign document of validation if the notary decide it 
    elif option == 4:
        exit = True
    else:
        print ("Choose a number among 1 and 3")
print ("Bye")
