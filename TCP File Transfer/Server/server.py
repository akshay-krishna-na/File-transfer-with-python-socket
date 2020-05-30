import socket
import threading
import os

def RetrFile(name, sock):
    filename = sock.recv(1024)
    if os.path.isfile(filename):
        filenamestr="FOUND"+str(os.path.getsize(filename))
        sock.send(filenamestr.encode('utf-8'))
        userResponse = sock.recv(1024).decode('utf-8')
        if userResponse[:2] == 'OK':
            with open(filename,'rb') as f:
                byteTosend = f.read(1024)
                sock.sendall(byteTosend)
                while (byteTosend):
                    byteTosend = f.read(1024)
                    sock.sendall(byteTosend)
    else:
        sock.send(b"ERR")
    sock.close()
def Main():
    host ="localhost"
    port =5007

    s = socket.socket()
    s.bind((host,port))
    s.listen(5)

    print("SERVER UP")

    while True:
        c,addr = s.accept()
        print("Client connected ! ")
        t=threading.Thread(target=RetrFile,args=("retrThread",c))
        t.start()
    s.close()

if __name__=="__main__":
    Main()

