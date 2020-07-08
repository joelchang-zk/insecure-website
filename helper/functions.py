import random
import secrets
import string
from datetime import datetime

from passlib.hash import sha256_crypt


def JSONSerialConvertor(obj):
    if isinstance(obj, datetime):
        return obj.__str__()
        
def genRandomId():
    alphabet = string.ascii_letters + string.digits
    id = ''.join(secrets.choice(alphabet) for i in range(8))
    return id

def getRandomAlphaNumericString(stringLength=8):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))

def allowed_file(filename, ALLOWED_EXTENSIONS):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def encryptFileName(filename):
    splitFile = filename.split(".")
    print(splitFile[0])
    print(splitFile[1])
    hashed = sha256_crypt.hash(splitFile[0])
    newStringOne = str(hashed).replace(".", "")
    newStringTwo = str(newStringOne).replace("/", "")
    newStringThree = str(newStringTwo).replace("\\", "")
    completeFileName = str(newStringThree) + "." + str(splitFile[1])
    return completeFileName
