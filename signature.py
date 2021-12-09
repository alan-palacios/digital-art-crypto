from Crypto.Hash import SHA256
from datetime import datetime

BLOCK_SIZE=512

def getAuthorMessage(name):
	today= datetime.now()
	message= f" This artwork was made by {name} - {today}"
	return message

def getAgreementMessage(name):
	today= datetime.now()
	message= f"Me, {name} agreed to not use this artwork without the consent of its author - {today}"
	return message

def hashDocument(filename):
	h = SHA256.new()
	with open(filename, 'rb') as f: # Open the file to read it's bytes
		fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
		while len(fb) > 0: # While there is still data being read from the file
			h.update(fb) # Update the hash
			fb = f.read(BLOCK_SIZE) # Read the next block from the file
	return h.hexdigest()

#FUNCTIONS:
#generate private and public passwords

#sign artwork and document of ownership
#verify artwork and document of ownership

#sign document of not use without authorization
#verify document of not use without authorization

#sign document of validation of both signatures
#verify document of validation of both signatures

#encrypt both documents