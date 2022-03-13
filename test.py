from threading import Thread
import time
import random
def printA():
    for i in range(5):
        print("A"+str(i)+"......")
        time.sleep(1)#random.randint(1,5)*0.1)
    return 89
 

def printB():
    for i in range(5):
        print("B"+str(i)+"*******")
        time.sleep(1)#random.randint(1,5)*0.1)
    return 89

def printAny(inarg):
    for i in range(5):
        print(str(inarg))



t1=Thread(target=printA)
intuple=(789,"HELLO",[1,2,3])
t2=Thread(target=printAny,args=(intuple,))
t1.start()
t2.start()
printB()

t1.join()
t2.join()

print("END")