from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import os
import socket





class MyWindow(QMainWindow):
    
    #functions for events

    def __init__(self):
        super(MyWindow,self).__init__()
        self.initUI()

    def button_clicked(self):
        host ="localhost"
        port = int(self.portaddr.text())

        s = socket.socket()
        self.update()
        s.bind((host,port))
        s.listen(5)
        c,addr = s.accept()
        filename = c.recv(1024)
        if os.path.isfile(filename):
            filenamestr="FOUND"+str(os.path.getsize(filename))
            c.send(filenamestr.encode('utf-8'))
            userResponse = c.recv(1024).decode('utf-8')
            if userResponse[:2] == 'OK':
                with open(filename,'rb') as f:
                    byteTosend = f.read(1024)
                    c.sendall(byteTosend)
                    while (byteTosend):
                        byteTosend = f.read(1024)
                        c.sendall(byteTosend)
        else:
            c.send(b"ERR")
        s.close()

    def initUI(self):

        #UI elements

        self.setGeometry(200, 200, 800, 300)
        self.setWindowTitle("TCP Server")

        self.label0 = QtWidgets.QLabel(self)
        self.label0.setText("port : ")
        self.label0.move(200,50)

        self.portaddr =QtWidgets.QLineEdit(self)
        self.portaddr.setGeometry(QtCore.QRect(300, 50, 341, 31))
        

        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText("Run Server")
        self.b2.setGeometry(350,120,100,30)
        self.b2.clicked.connect(self.button_clicked)

        self.sstatus = QtWidgets.QLabel(self)
        self.sstatus.setText("    ")
        self.sstatus.setGeometry(340,200,150,100)

    def update(self):
        self.sstatus.setText("TRANSFER COMPLETED")
        self.sstatus.adjustSize()


def main():

    
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

main()