#Server.py
from asyncio.windows_utils import BUFSIZE
import pickle
import socket
from TxBlock import TxBlock


TCP_PORT=5005
BUFFER_SIZE=1024
def newConnection(ip_addr):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((ip_addr,TCP_PORT))
    s.listen()
    return s
def recvObj(sock):
    new_sock,addr=sock.accept()
    all_data=b""
    while True:
        data=new_sock.recv(BUFFER_SIZE)
        if not data: break
        all_data=all_data+data
    return pickle.loads(all_data)


if __name__=="__main__":
    s=newConnection("192.168.148.74")
    newB=recvObj(s)
    print(newB.data[0])
    print(newB.data[1])

    if(newB.is_valid()):
        print("Success !! Tx is valid")
    else:
        print("ERROR !! tx invalid")

    if newB.data[0].inputs[0][1]==2.3:
        print("Success !! Input value matches")
    else:
        print("ERROR !! Wrong input value for block1,tx1 ")
    if newB.data[0].outputs[1][1]==1.1:
        print("Success !! Output value matches")
    else:
        print("ERROR !! Wrong Output value for block1,tx1 ")

    if newB.data[1].inputs[0][1]==2.3:
        print("Success !! Input value matches")
    else:
        print("ERROR !! Wrong input value for block1,tx1 ")

    if newB.data[1].inputs[1][1]==1.0:
        print("Success !! Input value matches")
    else:
        print("ERROR !! Wrong input value for block1,tx1 ")
    
    if newB.data[1].outputs[0][1]==3.1:
        print("Success !! Input value matches")
    else:
        print("ERROR !! Wrong input value for block1,tx1 ")

    newTX=recvObj(s)
    print(newTX)