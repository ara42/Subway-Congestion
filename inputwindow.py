import sys
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5 import uic
from PyQt5.QtGui import *
from routewindow import routewindow
from congestionwindow import congestionwindow

form_secondwindow = uic.loadUiType("input.ui")[0]

class secondwindow(QDialog,QWidget,form_secondwindow):
    def __init__(self):
        super(secondwindow,self).__init__()
        self.initUI()
        #self.showFullScreen()
        self.show()
        self.st1 =""
        self.st2 =""
        self.d =""
        self.h =""
        self.m =""
        
        pm = QPixmap('subway.png')
        pm = pm.scaled(self.label.width(),self.label.height())
        self.label.setPixmap(pm)
             
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    def initUI(self):
        self.setupUi(self)
        self.pb_put.clicked.connect(self.buttonClicked_put)
        self.pb_sr.clicked.connect(self.buttonClicked_sr)
        self.pb_re.clicked.connect(self.buttonClicked_re)

    def get_day(self):
        if self.r_mon.isChecked():
            return "월"
        if self.r_tue.isChecked():
            return "화"
        if self.r_wed.isChecked():
            return "수"
        if self.r_thur.isChecked():
            return "목"
        if self.r_fri.isChecked():
            return "금"
        if self.r_sat.isChecked():
            return "토"
        return "일"
        
    def buttonClicked_put(self):
        self.st1 =  self.l_start.text()
        self.st2 =  self.l_end.text()
        self.d = self.get_day()
        self.h = str(self.cb_time.currentText())+"시"
        self.m = str(self.cb_min.currentText())+"분"
              
        self.routewindow = routewindow(self.st1,self.st2,self.d,self.h,self.m)
        self.routewindow.exec() 
        self.show()
        
    def buttonClicked_sr(self):
        self.st1 =  self.l_start.text()
        self.st2 =  self.l_end.text()
        self.d = self.get_day()
        self.h = str(self.cb_time.currentText())+"시"
        self.m = str(self.cb_min.currentText())+"분"
             
        self.congestionwindow = congestionwindow(self.st1,self.st2,self.d,self.h,self.m)
        self.congestionwindow.exec() 
        self.show()
        
    def buttonClicked_re(self):
        self.close()
        
