#Blockchain
from cryptography.hazmat.primitives import hashes


class someClass:
    string=None
    num=536735
    def __init__(self,mystring):
        self.string=mystring

    def __repr__(self):
        return self.string+"|||"+str(self.num)
class CBlock:
    data=None
    previousHash=None
    previousBlock=None

    def __init__(self,data,previousBlock):
        self.data=data
        self.previousBlock=previousBlock
        if previousBlock!=None:
            self.previousHash=previousBlock.computeHash()
    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256())
        digest.update(bytes(str(self.data),"utf-8"))
        digest.update(bytes(str(self.previousHash),"utf-8"))
        return digest.finalize()


root=CBlock("I m Root",None)
B1=CBlock("I m child",root)
B2=CBlock("I m B1s brother",root)
B3=CBlock(12345,B1)
B4=CBlock(someClass("Hi There ! "),B2)
B5 = CBlock("Top block", B4)

for b in [B1,B2,B3,B4,B5]:
    if b.previousBlock.computeHash()==b.previousHash:
        print("Success!! Hash is good ")
    else:
        print("ERROR !! Hash is no good")
print(B4.data)
B4.data.num=12345
print(B4.data)
if B5.previousBlock.computeHash()==B4.previousHash:
    print("ERROR!!  couldn't detect tampering")
else:
    print("Sucess !! Tampering detected ")
 
 

