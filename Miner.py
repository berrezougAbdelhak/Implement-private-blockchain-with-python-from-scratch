from Transactions import Tx
import SocketUtils
from TxBlock import TxBlock

wallets=["localhost"]
tx_list=[]
def minerServer(my_ip,wallet_list):
    server=SocketUtils.newServerConnection(my_ip)
    for i in range(10):
        newTx=SocketUtils.recvObj(server)
        if isinstance(newTx,Tx):
            tx_list.append(newTx)
            print("Recd tx")
        else:
            print("Tx no recd")
        if len(tx_list)>=2:
            print("Tx_list>=2")
            break
    newBlock=TxBlock(None)
    newBlock.addTx(tx_list[0])
    newBlock.addTx(tx_list[1])
    for i in range(10):   
        print("Finding Nonce....") 
        newBlock.find_nonce()
        if newBlock.good_nonce():
            print("Good nonce found")
            break
    if not newBlock.good_nonce():
        print("ERROR !! couldn't find nonce")
        return False
    for ip_addr in wallet_list:
        print("Sending to"+ip_addr)
        SocketUtils.sendObj(ip_addr,newBlock,5006)


    
     
     
     
     
     #Open Server connection
     #Rec'v 2 transaction
     #collect into block
     #find nonce
     #send that block  to each in wallet_list



    return False



if __name__=="__main__":
    minerServer("localhost",wallets)
