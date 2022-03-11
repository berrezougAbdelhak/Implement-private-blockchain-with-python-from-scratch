import pickle
from plistlib import load
import random
import time
from turtle import pu
from Signature import generate_key, verify
from Signature import sign
from Transactions import Tx
from BlockChain import CBlock
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
class TxBlock(CBlock):
    reward =25.0
    nonce="AAAAAAA"
    leading_zeros=1
    next_char_limit=20
    def __init__(self,previousBlock):
        super(TxBlock,self).__init__([],previousBlock)

    def addTx(self,Tx_in):
        self.data.append(Tx_in)
    #Two underscore to say that is a private function of TxBlock and it shouldn't be use outside 
    def count_totals(self):
        total_in=0
        total_out=0
        for tx in self.data:
            for addr,amount in tx.inputs:
                total_in=total_in+amount

            for addr,amount in tx.outputs:
                total_out=total_out+amount
        return total_in,total_out

    def is_valid(self):
        if not  super(TxBlock,self).is_valid():
            return False
        for tx in self.data:
            if not tx.is_valid():
                return False
        total_in,total_out=self.count_totals()
        if total_out-total_in-TxBlock.reward>0.000000000000001:
            return False

        return True

    def good_nonce(self):
        digest = hashes.Hash(hashes.SHA256())
        digest.update(bytes(str(self.data),"utf-8"))
        digest.update(bytes(str(self.previousHash),"utf-8"))
        digest.update(bytes(str(self.nonce),"utf-8"))
        this_hash=digest.finalize()
        #print(this_hash[:self.leading_zeros])
        #print("this hash: ", str(this_hash[:self.leading_zeros]))
        #return this_hash[:self.leading_zeros]==bytes(''.join(["\x4f" for i in range(self.leading_zeros)]))
        if this_hash[:self.leading_zeros]!=bytes("".join(["\x00" for i in range(self.leading_zeros)]),"utf-8"):
            return False
        return int(this_hash[self.leading_zeros]<self.next_char_limit)
        
    def find_nonce(self):
        for i in range(100000):
            self.nonce=''.join([chr(random.randint(0,255)) for i in range(10*self.leading_zeros)])
            if self.good_nonce():
                return True
        return None


    




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
    start=time.time()
    print(B1.find_nonce())
    elapsed=time.time()-start
    print("elapsed time : "+str(elapsed) +" S.")
    if elapsed <60:
        print("ERROR ! mining is to fast ")


    


    if B1.good_nonce():
        print("Success !! nonce is good ")
    else:
        print("Error !! bad nonce")
    
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
    if load_B1.good_nonce():
        print("Success !! nonce is good after save and load !  ")
    else:
        print("Error! bad nonce after load !")
    #The miner 
    pr4, pu4 = generate_key()

    B2=TxBlock(B1)
    Tx5=Tx()
    Tx5.add_input(pu3,1)
    Tx5.add_output(pu1,100)
    Tx5.sign(pr3)
    B2.addTx(Tx5)
    load_B1.previousBlock.addTx(Tx4)

    for b in [B2,load_B1]:
        if b.is_valid():
            print("ERROR !  Bad block verifed ")
        
        else:
            print("Success !!  Bad block detected ")
    
    B3=TxBlock(B2)
    B3.addTx(Tx2)
    B3.addTx(Tx3)
    B3.addTx(Tx4)
    Tx6=Tx()
    Tx6.add_output(pu4,25)
    B3.addTx(Tx6)
    if B3.is_valid():
        print("Success !! block reward success ")
    else:
        print("ERROR !!  block reward fail ")
    
    

    B4=TxBlock(B3)
    B4.addTx(Tx2)
    B4.addTx(Tx3)
    B4.addTx(Tx4)
    Tx7=Tx()
    Tx7.add_output(pu4,25.2)
    B4.addTx(Tx7)
    if B4.is_valid():
        print("Success !! Tx fees  success ")
    else:
        print("ERROR !!  Tx fees  fail ")

    #Greedy Mind 
    B5=TxBlock(B4)
    B5.addTx(Tx2)
    B5.addTx(Tx3)
    B5.addTx(Tx4)
    Tx8=Tx()
    Tx8.add_output(pu4,26)
    B5.addTx(Tx8)
    if not B5.is_valid():
        print("Success !! Greedy miner detected ")
    else:
        print("ERROR !!  Greedy miner not detected ")



