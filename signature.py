from Crypto.Hash import SHA256
from datetime import datetime
from base64 import b64encode # or urlsafe_b64decode

BLOCK_SIZE=512

def getAuthorMessage(name, filename):
	today= datetime.now()
	message= f"The artwork located in {filename} was made by {name} - {today}|{name}|{filename}"
	return message

def getAgreementMessage(name, artist_name):
	today= datetime.now()
	message= f"Me, {name} agreed to not use this artwork without the consent of its author {artist_name} - {today}|{name}|{artist_name}"
	return message

def hashDocument(filename, hash_file):
	h = SHA256.new()
	with open(filename, 'rb') as f: # Open the file to read it's bytes
		fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
		while len(fb) > 0: # While there is still data being read from the file
			h.update(fb) # Update the hash
			fb = f.read(BLOCK_SIZE) # Read the next block from the file
	with open(hash_file, 'wb') as fo:
		fo.write(b64encode(h.digest()))
	return b64encode(h.digest())

def hashData(data, hash_file):
	data = bytes(data, 'utf-8')
	h = SHA256.new()
	h.update(data) # Update the hash
	with open(hash_file, 'wb') as fo:
		fo.write(b64encode(h.digest()))
	return b64encode(h.digest())
#FUNCTIONS:
#generate private and public passwords

#sign artwork and document of ownership
#verify artwork and document of ownership

#sign document of not use without authorization
#verify document of not use without authorization

#sign document of validation of both signatures
#verify document of validation of both signatures

#encrypt both documents