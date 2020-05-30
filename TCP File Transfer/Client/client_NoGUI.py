import socket
def Main():
    host = "localhost"
    port = 5000

    s=socket.socket()
    s.connect((host,port))

    filename = input("Enter Filename (or enter q to quit): ")
    if filename != 'q':
        s.send(filename.encode('utf-8'))
        data = s.recv(1024)
        data = data.decode('utf-8')
        if data[:5] == "FOUND":
            filesize=int(data[5:])
            message = input("File Exists, "+str(filesize)+ "Bytes, download ?(y/n):")

            if message == 'y':
                s.send(b"OK")
                f = open("new_"+filename,'wb')
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                print("File Downloaded ! ")

        else:
            print("File doesn't exixt ! ")

if __name__ == "__main__":
    Main()


