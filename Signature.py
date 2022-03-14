from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import  rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
def generate_key():
    private=rsa.generate_private_key(public_exponent=65537,key_size=2048,backend=default_backend()
                                     )
    public=private.public_key()

    pu_ser = public.public_bytes(
   encoding=serialization.Encoding.PEM,
   format=serialization.PublicFormat.SubjectPublicKeyInfo
    )   

    return private,pu_ser

def sign(message,private):
    message=bytes(str(message),"utf-8")
    sig = private.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return sig

def verify(message,sig,pu_ser):
    
    
    public = serialization.load_pem_public_key(
        pu_ser
        )
    message=bytes(str(message),"utf-8")
    try:
        public.verify(
            sig,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
         )
        #print("Signature compatible")
        return True
    except InvalidSignature:
        return False
    except:
        print("Error executing public_key.verify")
        return False

def savePrivate(pr_key,filename):
    pem = pr_key.private_bytes(
   encoding=serialization.Encoding.PEM,
   format=serialization.PrivateFormat.PKCS8,
   encryption_algorithm=serialization.BestAvailableEncryption(b'mypassword')
    )
    fp=open(filename,"wb")
    fp.write(pem)
    fp.close()
    return True

def loadPrivate(filename):
    fin=open(filename,"rb")
    pr_key = serialization.load_pem_private_key(
        fin.read(),
        password=b'mypassword',
    )
    fin.close()
    return pr_key
def savePublic(pu_key,filename):
    fp=open(filename,"wb")
    fp.write(pu_key)
    fp.close()

    return True

def loadPublic(filename):
    fin=open(filename,"rb")
    pu_key=fin.read()
    fin.close()
    return pu_key
 
    
   


if __name__ == "__main__":
    pr,pu=generate_key()
    print(pr)
    print(pu)
    message=b"This is a secret message"
    sig=sign(message,pr)
    print(sig)
    verif=verify(message,sig,pu)
    print("Sign in the first one : ",verif)

    pr2,pu2=generate_key()
    sig2=sign(message,pr2)
    print(verify(message,sig2,pu))

    bad_message=message+b"Q"
    print("Altering the message : ",verify(bad_message,sig,pu))
    
    savePrivate(pr2,"private.key")
    pr_load=loadPrivate("private.key")
    sig3=sign(message,pr_load)
    correct=verify(message,sig3,pu2)

    if correct:
        print("Succcess !! Good loaded private key")
    else:
        print("ERROR ! load private key is bad ")

    savePublic(pu2,"public.key")
    pu_load=loadPublic("public.key")

    correct=verify(message,sig3,pu_load)

    if correct:
        print("Success !! Good loaded key")
    else:
        print("ERROR!! load public key is bad ")

