import sys
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5 import uic
import pandas as pd
import webbrowser

form_informwindow = uic.loadUiType("inform.ui")[0]
inform_list = pd.read_csv('inform.csv',encoding='cp949')

class informwindow(QDialog,QWidget,form_informwindow):
    def __init__(self):
        super(informwindow,self).__init__()
        self.initUI()
        self.show()
        
        for line in range(1, 10):
            self.li_line.addItem(f'{line}호선')

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    def initUI(self):
        self.setupUi(self)
        self.li_line.itemClicked.connect(self.Clicked_line)
        self.li_station.itemDoubleClicked.connect(self.doubleClicked_station)
        self.pb_re.clicked.connect(self.buttonClicked_re)
        
    def Clicked_line(self):
        self.li_station.clear()
        c_line = self.li_line.currentItem().text()
        line = c_line[0]
        line = int(line)
        index_station = inform_list.index[(inform_list['호선'] == line)].tolist()

        for i in range(len(index_station)):
            self.li_station.addItem(inform_list['역명'][index_station[i]])
        
    def doubleClicked_station(self):
        clicked_station = self.li_station.currentItem().text()
        index_number = inform_list.index[(inform_list['역명'] == clicked_station)].tolist()
        station = inform_list['이미지명'][index_number[0]]
        url = f"http://data.seoul.go.kr/contents/stn_img/{station}"
        webbrowser.open(url)
              
    def buttonClicked_re(self):
        self.close()

