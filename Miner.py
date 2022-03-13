from ast import arg
from concurrent.futures import thread
import Transactions 
import SocketUtils
from TxBlock import TxBlock
import Signature
from threading import Thread
wallets=[("localhost",5005)]
tx_list=[]
head_blocks=[None]
def findLonguestBlockchain():
    longuest=-1
    long_head=None
    for b in head_blocks:
        current=b
        this_len=0
        while current!=None:
            this_len=this_len+1
            current=current.previousBlock
        if this_len>longuest:
            long_head=b
            longuest=this_len
    return long_head

def minerServer(my_addr):
    my_ip,my_port=my_addr
    server=SocketUtils.newServerConnection(my_ip,my_port)
    #Get 2 Tx from wallet

    for i in range(10):
        newTx=SocketUtils.recvObj(server)
        if isinstance(newTx,Transactions.Tx):
            tx_list.append(newTx)
            print("Recd tx")
        else:
            print("Tx no recd")
        if len(tx_list)>=2:
            print("Tx_list>=2")
            break
    
     #Open Server connection
     #Rec'v 2 transaction
     #collect into block
     #find nonce
     #send that block  to each in wallet_list
    return False

def nonceFinder(wallet_list,miner_public):
    #add Tx to new block 
    newBlock=TxBlock(findLonguestBlockchain())
    newBlock.addTx(tx_list[0])
    newBlock.addTx(tx_list[1])
    #Compute and add mining reward 
    total_in,total_out=newBlock.count_totals()
    mine_reward=Transactions.Tx()
    mine_reward.add_output(my_public,25.0+total_in-total_out)
    newBlock.addTx(mine_reward)
    #Fine the nonce 
    for i in range(10):   
        print("Finding Nonce....") 
        newBlock.find_nonce()
        if newBlock.good_nonce():
            print("Good nonce found")
            break
    if not newBlock.good_nonce():
        print("ERROR !! couldn't find nonce")
        return False
    #Send new block
    for ip_addr in wallet_list:
        print("Sending to"+ip_addr)
        SocketUtils.sendObj(ip_addr,newBlock,5006)
    head_blocks.remove(newBlock.previousBlock)
    head_blocks.append(newBlock)


    return True

if __name__=="__main__":
    my_pr,my_pu=Signature.generate_key()
    t1=Thread(target=minerServer,args=(("localhost",5005),))
    t2=Thread(target=nonceFinder,args=(wallets,my_pu))
    t1.start()
    t2.start()
    pr1,pu1=Signature.generate_key()
    pr2,pu2=Signature.generate_key()
    pr3,pu3=Signature.generate_key()

    Tx1=Transactions.Tx()
    Tx2=Transactions.Tx()

    Tx1.add_input(pu1,4.0)
    Tx1.add_input(pu2,1.0)
    Tx1.add_output(pu3,4.8)
    Tx2.add_input(pu3,4.0)
    Tx2.add_output(pu2,4.0)
    Tx2.add_reqd(pu1)

    Tx1.sign(pr1)
    Tx1.sign(pr2)
    Tx2.sign(pr3)
    Tx2.sign(pr1)

    try:
        SocketUtils.sendObj("localhost",Tx1)
        print("Sent Tx1")
        SocketUtils.sendObj("localhost",Tx2)
        print("Sent Tx2")
    except :
        print("Error !! Connection unsuccessful")
    server=SocketUtils.newServerConnection("localhost",5006)

    for i in range(30):
        newBlock=SocketUtils.recvObj(server)
        if newBlock:
            break
    server.close()

    if newBlock.is_valid():
        print("Success !! Block is valid ")

    if newBlock.good_nonce():
        print("Success !! nonce is valid  ")

    print(Tx1.is_valid())
    print(Tx2.is_valid())
    for tx in newBlock.data:
        #Try parce que miner reward n'a pas d'inputs donc une erruer out bound of range 
        try:
            if tx.inputs[0][0] == pu1 and tx.inputs[0][1] == 4.0:
                print("Tx1 is present ")
        except:
            pass
        try:
            if tx.inputs[0][0] ==pu3 and tx.inputs[0][1]==4.0:
                print("Tx2 is present ")
        except:
            pass





    t1.join()
    t2.join()
    print(head_blocks[0])