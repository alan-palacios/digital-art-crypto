import signature
import AES

key = b'12345678901234567890123456789012'
ciphertext = AES.encrypt(key,'holi')
print(ciphertext)
print(AES.decrypt(key,ciphertext))
print(signature.hashDocument('sampleText.txt'))
print(signature.getAgreementMessage('Bob'))

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
        print ("Option 1")
		#for alice:
		#sign artwork previously requesting the name of the artist and showing the message of ownership that will be added:
		#verify final document received by notary
		#show final document
    elif option == 2:
        print ("Option 2")
		#for bob:
		#verify and show document received by alice
		#sign document of not use without authorization previosly requesting the name
		#verify final document received by notary
		#show final document
    elif option == 3:
        print("Option 3")
		#for notary:
		#verify and show document received by bob and alice
		#sign document of validation if the notary decide it 
    elif option == 4:
        exit = True
    else:
        print ("Choose a number among 1 and 3")
print ("Bye")
