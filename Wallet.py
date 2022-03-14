from http import server
from time import time
import SocketUtils
from TxBlock import TxBlock
import Transactions
import Signature
from threading import Thread
import time
import Miner
head_blocks=[None]
wallets=[("localhost",5006)]
miners=[("localhost",5005)]
break_now=False









def walletServer(my_addr):
    server=SocketUtils.newServerConnection("localhost",5006)
    while not break_now:
        newBlock=SocketUtils.recvObj(server)
        print("Recv'd block")

        if isinstance(newBlock,TxBlock):
            for b in head_blocks:
                if b==None:
                    if newBlock.previousHash==None:
                        newBlock.previousBlock=b
                        head_blocks.remove(b)
                        head_blocks.append(newBlock)    
                        print(" Added to head blocks")
                        
                elif newBlock.previousHash==b.computeHash():
                    newBlock.previousBlock=b
                    head_blocks.remove(b)
                    head_blocks.append(newBlock)
                    print(" Added to head blocks")
                #ToDo what if i add to an earlier (non-head) block ?


    server.close()
    return True
def getBalance(pu_key):

    return 0.0

def sendCoins(pu_send,amt_send,pr_send,pu_recv,amt_recv,miner_list):
    return True

if __name__=="__main__":
    miner_pr,miner_pu=Signature.generate_key()
    t1=Thread(target=Miner.minerServer,args=(("localhost",5005),))
    t2=Thread(target=Miner.nonceFinder,args=(wallets,miner_pu))
    t3=Thread(target=walletServer,args=(('localhost',5006),))

    t1.start()
    t2.start()
    t3.start()
    
    pr1,pu1=Signature.generate_key()
    pr2,pu2=Signature.generate_key()
    pr3,pu3=Signature.generate_key()

    #Query balance
    bal1=getBalance(pu1)
    bal2=getBalance(pu2)
    bal3=getBalance(pu3)

    #Send coins 
    sendCoins(pu1,1.0,pr1,pu2,1.0,miners)
    sendCoins(pu1,1.0,pr1,pu3,0.3,miners)

    time.sleep(30)
    
    #Query balance
    new1=getBalance(pu1)
    new2=getBalance(pu2)
    new3=getBalance(pu3)

    #Veify Balance

    if abs(new1-bal1+1.3)>0.00000001:
        print("Error ! wrong balance  for pu1")
    
    else:
        print("Success good balance for pu1")
    if abs(new2-bal2-1.0)>0.00000001:
        print("Error ! wrong balance  for pu2")
    
    else:
        print("Success good balance for pu2")
    if abs(new3-bal3-0.3)>0.00000001:
        print("Error ! wrong balance  for pu3")
    
    else:
        print("Success good balance for pu3")

    Miner.break_now=True    
    break_now=True




    t1.join()
    t2.join()
    t3.join()

    print("Exit Successfule")

