import sys
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5 import uic
from PyQt5.QtGui import *
from subway_route import route

form_routewindow = uic.loadUiType("route.ui")[0]

class routewindow(QDialog,QWidget,form_routewindow):
    def __init__(self, ST1, ST2, D, H, M):
        super(routewindow,self).__init__()
        self.initUI()
        self.show()

        RT, LT = route(ST1, ST2, D, H, M)
        RT = list((RT))
        
        li_station = []
        li_line = []
        f_line = RT[0][2].split()[0]
        li_line.append(f_line)
        
        pm = QPixmap('route.png')
        pm = pm.scaled(self.label_6.width(),self.label_6.height())
        self.label_6.setPixmap(pm)
        
        cnt = 0
        for station,time,line in RT:
            cnt += 1
            station = station+"역"
            line = line.split()[0]
            
            nr = self.table.rowCount()
            self.table.setRowCount(nr+1)
            self.table.setItem(nr,0,QTableWidgetItem(station))
            self.table.setItem(nr,1,QTableWidgetItem(time))
            self.table.setItem(nr,2,QTableWidgetItem(line))

            if f_line != line:
                li_station.append(station)
                li_line.append(line)
                f_line = line               
        
        if len(li_station) > 0:
            for i in range(len(li_station)):
                self.lw_trans.addItem(f'{li_station[i]}에서')
                self.lw_trans.addItem(f'{li_line[i]} -> {li_line[i+1]} 환승')
        else: 
            self.lw_trans.addItem("환승역이 없습니다")
     
        self.lineEdit.setText(LT)
        self.lineEdit_2.setText(RT[0][1])
        self.lineEdit_3.setText(RT[-1][1])
        self.lineEdit_4.setText(str(cnt))
            
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    def initUI(self):
        self.setupUi(self)
        self.set_table()
        self.button_re.clicked.connect(self.buttonClicked_re)
        
    def set_table(self):
        self.table.setColumnCount(3)
        columns = ["역명","시간","호선"]
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setColumnWidth(0,250)
        self.table.setColumnWidth(1,100)
        self.table.setColumnWidth(2,120)
        
    def buttonClicked_re(self):
        self.close()