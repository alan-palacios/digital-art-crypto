import base64
  
def image2str(img):
    with open(img, "rb") as image2string:
        converted_string = base64.b64encode(image2string.read())
    return converted_string 

def saveFile(fileBin, s):
    with open(fileBin, "wb") as file:
        file.write(s)
        file.close()

def readBin(fileBin):
    file = open(fileBin, 'rb')
    byte = file.read()
    file.close()
    return byte

def str2img(byte, imgFile):  
    byte = byte[2:len(byte)-1]
    decodeit = open(imgFile, 'wb')
    decodeit.write(base64.b64decode((byte)))
    decodeit.close()