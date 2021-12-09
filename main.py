#MENU:
#for alice:
#sign artwork previously requesting the name of the artist and showing the message of ownership that will be added:
#verify final document received by notary
#show final document

#for bob:
#verify and show document received by alice
#sign document of not use without authorization previosly requesting the name
#verify final document received by notary
#show final document

#for notary:
#verify and show document received by bob and alice
#sign document of validation if the notary decide it 

import signature
print(signature.hashDocument('sampleText.txt'))
print(signature.getAgreementMessage('Bob'))