import pickle
from plistlib import load
from Signature import generate_key, verify
from Signature import sign
from Transactions import Tx
from BlockChain import CBlock
from cryptography.hazmat.primitives import serialization
class TxBlock(CBlock):

    def __init__(self,previousBlock):
        pass
    def addTx(self,Tx_in):
        pass
    def is_valid(self):
        return False

if __name__=="__main__":
    pr1, pu1 = generate_key()
    pr2, pu2 = generate_key()
    pr3, pu3 = generate_key()

    Tx1 = Tx()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.sign(pr1)

    if Tx1.is_valid():
        print("Success! Tx is valid")

    savefile=open("tx.dat","wb")
    pickle.dump(Tx1,savefile)
    savefile.close()

    loadfile=open("tx.dat","rb")
    newTx=pickle.load(loadfile)
    loadfile.close()

    if (newTx.is_valid()):
        print("Success !! New Tx is valid ")


        