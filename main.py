import sys
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5 import uic
from PyQt5.QtGui import *
from inputwindow import secondwindow
from informwindow import *

form_main = uic.loadUiType("firstwindow.ui")[0] #ui 파일 불러오기

class MainWindow(QMainWindow,QWidget,form_main):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.f_inform.clicked.connect(self.buttonClicked_inform)  # 역 정보 클릭시 연결되는 함수
        self.f_search.clicked.connect(self.buttonClicked_search)  # 노선 정보 클릭시 연결되는 함수
        self.f_exit.clicked.connect(self.buttonClicked_exit) # 종료 클릭시 연결되는 함수

    def buttonClicked_inform(self):
        self.inform = informwindow()
        self.inform.exec() 
        self.show()

    def buttonClicked_search(self):
        self.second = secondwindow()
        self.second.exec() 
        self.show()
        
    def buttonClicked_exit(self):
        self.close() 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()