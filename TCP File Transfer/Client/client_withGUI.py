from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import socket





class MyWindow(QMainWindow):

    host = "localhost"
    port = 0000
    s=socket.socket()
    
    filename = ''
    filesize = 0
    
    #functions for events

    def __init__(self):
        super(MyWindow,self).__init__()
        self.initUI()

    def button_clicked(self):
        self.port = int(self.portaddr.text())
        self.s.connect((self.host,self.port))
        self.filename = self.fname.text()
        if self.filename == '':
            self.fstatus.setText("File Not Found !")
            self.update()

        self.s.send(self.filename.encode('utf-8'))
        data = self.s.recv(1024)
        data = data.decode('utf-8')
        if data[:5] == "FOUND":
            self.filesize=int(data[5:])
            self.fstatus.setText("         File Exist !\n      "+str(self.filesize)+ " bytes\nReady to Download")
            self.update()
        #self.fstatus.setText(text)
        else:
            self.fstatus.setText("File Not Found !")
            self.update()
        

    def button_clicked2(self):
        #download button action here
        self.s.send(b"OK")
        f = open("new_"+self.filename,'wb')
        data = self.s.recv(1024)
        totalRecv = len(data)
        f.write(data)
        while totalRecv < self.filesize:
            data = self.s.recv(1024)
            totalRecv += len(data)
            f.write(data)
        self.dstatus.setText("Downloaded ! ")
        self.update()
    

    def initUI(self):

        #UI elements

        self.setGeometry(200, 200, 800, 500)
        self.setWindowTitle("TCP Client")

        self.label0 = QtWidgets.QLabel(self)
        self.label0.setText("port : ")
        self.label0.move(200,50)

        self.portaddr =QtWidgets.QLineEdit(self)
        self.portaddr.setGeometry(QtCore.QRect(300, 50, 341, 31))

        self.label = QtWidgets.QLabel(self)
        self.label.setText("Filename : ")
        self.label.move(200,100)

        
        self.fname =QtWidgets.QLineEdit(self)
        self.fname.setGeometry(QtCore.QRect(300, 100, 341, 31))
        


        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Check File")
        self.b1.move(350,150)
        self.b1.clicked.connect(self.button_clicked)

        self.fstatus = QtWidgets.QLabel(self)
        self.fstatus.setText("    ")
        self.fstatus.setGeometry(340,200,150,100)

        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText("Download File")
        self.b2.setGeometry(330,350,150,30)
        self.b2.clicked.connect(self.button_clicked2)

        self.dstatus = QtWidgets.QLabel(self)
        self.dstatus.setText("    ")
        self.dstatus.setGeometry(350,400,150,30)

    def update(self):
        self.label.adjustSize()


def main():

    
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

main()