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