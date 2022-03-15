from ast import arg
from concurrent.futures import thread
from glob import glob
from sqlite3 import Time
import Transactions 
import SocketUtils
import TxBlock

wallets=[("localhost",5006)]
tx_list=[]
head_blocks=[None]
break_now=False
verbose=False
def stopAll():
    global break_now
    break_now=True
def minerServer(my_addr):
    global tx_list
    global break_now
    head_blocks=[None]
    my_ip,my_port=my_addr
    server=SocketUtils.newServerConnection(my_ip,my_port)

    #Get Tx from wallet
    while not break_now:
        newTx=SocketUtils.recvObj(server)
        if isinstance(newTx,Transactions.Tx):
            tx_list.append(newTx)
            if verbose:
                print("Recd tx")
        else:
            print("Tx no recd")
    
     #Open Server connection
     #Rec'v 2 transaction
     #collect into block
     #find nonce
     #send that block  to each in wallet_list
    return False

def nonceFinder(wallet_list,miner_public):
    #add Tx to new block 
    global break_now
    while not break_now:
        newBlock=TxBlock.TxBlock(TxBlock.TxBlock.findLonguestBlockchain(head_blocks))
        for tx in tx_list:
            newBlock.addTx(tx)
        #Compute and add mining reward 
        total_in,total_out=newBlock.count_totals()
        mine_reward=Transactions.Tx()
        mine_reward.add_output(miner_public,25.0+total_in-total_out)
        newBlock.addTx(mine_reward) 
        #Fine the nonce 
        PRT=5006
        if verbose:  
            print("Finding Nonce....") 
        newBlock.find_nonce(10000)
        if newBlock.good_nonce():
            if verbose:
                print("Good nonce found")
            
            head_blocks.remove(newBlock.previousBlock)
            head_blocks.append(newBlock)
            #Send new block
            savePrevious=newBlock.previousBlock
            newBlock.previousBlock=None

            for ip_addr,port in wallet_list:
                if verbose:
                    print("S ending to"+ip_addr+ ":" + str(port))
                SocketUtils.sendObj(ip_addr,newBlock,5006)
            newBlock.previousBlock=savePrevious
            #Remove used tvs from tx_list 
            for tx in newBlock.data:
                if tx!=mine_reward:
                    tx_list.remove(tx)

    return True
import pickle
def loadTxList(filename):
    fin=open(filename,"rb")
    ret=pickle.load(fin)
    fin.close()
    return ret
    
    
def saveTxList(the_list,filename):
    fp=open(filename,"wb")
    pickle.dump(the_list,fp)
    fp.close
    return True




if __name__=="__main__":
    import time
    import Signature
    from threading import Thread
    my_pr,my_pu=Signature.generate_key()
    t1=Thread(target=minerServer,args=(("localhost",5005),))
    t2=Thread(target=nonceFinder,args=(wallets,my_pu))

    server=SocketUtils.newServerConnection("localhost",5006)
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

    new_tx_list=[Tx1,Tx2]
    saveTxList(new_tx_list,"Txs.dat")
    new_new_tx_list=loadTxList("Txs.dat")
    
    for tx in new_tx_list:

        try:
            SocketUtils.sendObj("localhost",tx)
            print("Sent Tx")
            
        except :
            print("Error !! Connection unsuccessful")

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
    print("rani nelhag hna ")
    for tx in newBlock.data:
        try:
            if tx.inputs[0][0] == pu1 and tx.inputs[0][1] == 4.0:
                print("Tx1 is present")
        except:
            pass
        try:
            if tx.inputs[0][0] == pu3 and tx.inputs[0][1] == 4.0:
                print("Tx2 is present")
        except:
            pass

    time.sleep(20)
    break_now=True
    time.sleep(2)
    server.close()





    t1.join()
    t2.join()

    print("Done")