import socket
import pickle
import select

TCP_PORT=5005
def sendObj(ip_addr,inObj,port=TCP_PORT):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip_addr,port))
    data=pickle.dumps(inObj)
    s.send(data)
    s.close()
    return False

TCP_PORT=5005
BUFFER_SIZE=1024
def newServerConnection(ip_addr,port=TCP_PORT):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((ip_addr,port))
    s.listen()
    return s
def recvObj(sock):
    inputs,outputs,error=select.select([sock],[],[sock],6)
    if sock in inputs:
        new_sock,addr=sock.accept()
        all_data=b""
        while True:
            data=new_sock.recv(BUFFER_SIZE)
            if not data: break
            all_data=all_data+data
        return pickle.loads(all_data)
    return None

if __name__=="__main__":
    server=newServerConnection("localhost")
    O=recvObj(server)
    print("Success!!")
    print(O)
    server.close()
