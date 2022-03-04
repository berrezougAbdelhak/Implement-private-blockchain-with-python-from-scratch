import pickle
from plistlib import load
from turtle import pu
from Signature import generate_key, verify
from Signature import sign
from Transactions import Tx
from BlockChain import CBlock
from cryptography.hazmat.primitives import serialization
class TxBlock(CBlock):

    def __init__(self,previousBlock):
        super(TxBlock,self).__init__([],previousBlock)

    def addTx(self,Tx_in):
        self.data.append(Tx_in)
    def is_valid(self):
        if not  super(TxBlock,self).is_valid():
            return False
        return True


if __name__=="__main__":
    pr1, pu1 = generate_key()
    pr2, pu2 = generate_key()
    pr3, pu3 = generate_key()

    Tx1 = Tx()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.sign(pr1)

    if Tx1.is_valid():
        print("Success! Tx1 is valid")

    savefile=open("tx.dat","wb")
    pickle.dump(Tx1,savefile)
    savefile.close()

    loadfile=open("tx.dat","rb")
    newTx=pickle.load(loadfile)
    loadfile.close()

    if (newTx.is_valid()):
        print("Success !! Loaded Tx is valid ")

    root=TxBlock(None)
    root.addTx(Tx1)

    Tx2=Tx()
    Tx2.add_input(pu2,1.1)
    Tx2.add_output(pu3,1)
    Tx2.sign(pr2)
    root.addTx(Tx2)

    B1=TxBlock(root)
    Tx3=Tx()
    Tx3.add_input(pu3,1.1)
    Tx3.add_output(pu1,1)
    Tx3.sign(pr3)

    B1.addTx(Tx3)

    Tx4=Tx()
    Tx4.add_input(pu1,1)
    Tx4.add_output(pu2,1)
    Tx4.add_reqd(pu3)
    Tx4.sign(pr1)
    Tx4.sign(pr3)
    B1.addTx(Tx4)

    savefile=open("block.dat","wb")
    pickle.dump(B1,savefile)
    savefile.close()

    loadfile=open("block.dat","rb")
    load_B1=pickle.load(loadfile)

    
    for b in [root,B1,load_B1,load_B1.previousBlock]:
        
        if b.is_valid():
            print("Success !! block is valid ")

        else:
            print("ERROR !! block is not valid ")

    B2=TxBlock(B1)
    Tx5=Tx()
    Tx5.add_input(pu3,1)
    Tx5.add_output(pu1,100)
    Tx5.sign(pr3)

    load_B1.previousBlock.addTx(Tx4)

    for b in [B2,load_B1]:
        if b.is_valid():
            print("ERROR !  Bad block verifed ")
        
        else:
            print("Success !!  Bad block detected ")
    
    













