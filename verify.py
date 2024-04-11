import hashlib
import rsa
import base64
import requests
import json


PUBLICKEY = requests.get('https://cliauth.repl.co/pubkey.pem').text.encode()
SIGNING_ALGORITHM = "SHA256"
print(PUBLICKEY)


def getSignature(rawdata):
#  # Converting string to bytes
  data = rawdata.encode('utf-8')
#  # Sign the data and return the signature
  signature = rsa.sign(data, private_key, SIGNING_ALGORITHM)
  return signature

def getValid():
  return requests.get('https://cliauth.repl.co/auth.json').json()

def verifySignature(rawdata, rawSignature, publicKeyString):
  #print(rawdata)
  #print(rawdata.encode())
  #print(rawSignature)
  try:
    # Verifying signature using rsa.verify() function
    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(publicKeyString)
    #print(public_key)
    isVerified = rsa.verify(rawdata.encode(), 
                            rawSignature, 
                            public_key)
    return True
  except rsa.pkcs1.VerificationError:
    return False

def getAuth(auth):
  auth = json.loads(auth)
  if verifySignature(auth.get("payload"), base64.b64decode(auth.get("signature")), PUBLICKEY) and json.loads(auth.get("payload", "{}")).get("authid") in getValid().get(json.loads(auth.get("payload", "{}")).get("id")):
    #raise Exception(getValid().get(json.loads(auth.get("payload", "{}")).get("id")))
    return json.loads(auth["payload"])
  else:
    raise Exception(f'Signature is not valid')
