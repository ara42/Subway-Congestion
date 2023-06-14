import sys
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5 import uic
from PyQt5.QtGui import QColor
from subway_congestion import *

form_congestionwindow = uic.loadUiType("congestion.ui")[0]

class congestionwindow(QDialog,QWidget,form_congestionwindow):
    def __init__(self, ST1, ST2, D, H, M):
        super(congestionwindow,self).__init__()
        self.initUI()
        self.show()     
        
        st_na, sst, cong, spst, RT, df = RST(ST1, ST2, D, H, M) 
        self.tb_con(cong, RT)
        self.tb_an(st_na, cong, sst, df, spst)
        
        
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
   
    def initUI(self):
        self.setupUi(self)
        self.set_table()
        
        self.button_re2.clicked.connect(self.buttonClicked_re2)
        
    def set_table(self):
        self.table.setColumnCount(13)
        columns = ["역명","시간","호선","1호차","2호차","3호차","4호차","5호차",
                   "6호차","7호차","8호차","9호차","10호차"]
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setColumnWidth(0,230)
        self.table.setColumnWidth(1,100)
        self.table.setColumnWidth(2,150)
        for i in range(10):
            self.table.setColumnWidth(i+3,70)
            
    def tb_con(self, cong, RT):
        cnt = -1
        for station,time,line in RT:
            cnt += 1
            station = station+"역"
            line = line.split()[0]
            
            nr = self.table.rowCount()
            self.table.setRowCount(nr+1)
            self.table.setItem(nr,0,QTableWidgetItem(station))
            self.table.setItem(nr,1,QTableWidgetItem(time))
            self.table.setItem(nr,2,QTableWidgetItem(line))
            for i in range(10):
                cong_item = QTableWidgetItem()
                if cong[cnt][i] == "여유":
                    cong_item.setBackground(QColor(76, 248, 106))
                elif cong[cnt][i] == "보통":
                    cong_item.setBackground(QColor(63, 185, 241))
                elif cong[cnt][i] == "주의":
                    cong_item.setBackground(QColor(255, 191, 39) )
                elif cong[cnt][i] == "혼잡":
                    cong_item.setBackground(QColor(247, 95, 115))                    
                self.table.setItem(nr,i+3,cong_item)
                
                
                
    def Split(self, aa, spst):
        s = 0
        re=[]
        for e in spst:
            re.append(aa[s:e])
            s = e
        re.append(aa[s:len(aa)])
        return re
    
    def tb_an(self, st_na, cong, sst, df, spst):
        self.table_an.setColumnCount(1)
        columns = [""]
        self.table_an.setHorizontalHeaderLabels(columns)
        self.table_an.setColumnWidth(0,1000)
        
        k1=self.Split(st_na,spst)
        k2=self.Split(cong,spst)
        k3=self.Split(sst,spst)
        k4=self.Split(df[2],spst)
    
      
        for h in range(len(k1)):
            p_line = k4[h].values[0]
            print(p_line)
            nmean=[]
            for i in k3[h]:
                lnn=0
                for j in i:
                    if j!=0:
                        lnn+=1
                if sum(i)==0:
                    nmean.append(0)
                else:
                    lnen=sum(i)/lnn
                    nmean.append(lnen)
         
            
            if len(nmean)==1:
                if sum(nmean)==0:
                    kk1=str(k1[h]).replace(',','->')
                    kk1=kk1.replace('[[','')
                    kk1=kk1.replace(']]','')
                    
                    sen1 = f'{p_line.split()[0]} ({k1[h][0]} -> {k1[h][-1]})'
                    sen2 = f'혼잡도를 지원하지 않는 노선입니다.'
                    
                    nr2 = self.table_an.rowCount()
                    self.table_an.setRowCount(nr2+2)
                    item_sen1 = QTableWidgetItem(sen1)
                    item_sen1.setBackground(QColor(76, 248, 106))
                    self.table_an.setItem(nr2,0,item_sen1)
                    self.table_an.setItem(nr2+1,0,QTableWidgetItem(sen2))
                    
                else: ##역 하나일 때는 칸혼잡도 정보만 출력
                    lii=k3[h]
                    list_data=[]
                    for j in lii:
                        li = [i for i in j if i!=0]
                        list_data.append(li)
                    sld = sorted(list_data[0])
                
                    small_values = sld[:2]
                    large_values = sld[-2:]
                    
                    if small_values[0] == small_values[1]:
                        small_values2 = list(filter(lambda x: list_data[0][x] == small_values[0], range(len(list_data[0]))))
                    else:
                        small_values2 = [list_data[0].index(value) for value in small_values]
                
                    if large_values[0] == large_values[1]:
                        large_values2 = list(filter(lambda x: list_data[0][x] == large_values[0], range(len(list_data[0]))))
                    else:
                        large_values2 = [list_data[0].index(value) for value in large_values]
                    
                    sen1 = f'{p_line.split()[0]} ({k1[h][0]})'
                    sen2 = f'{large_values2[0]+1},{large_values2[1]+1}칸에서 가장 많은 혼잡이 예상되며, '
                    sen3 = f'{small_values2[0]+1},{small_values2[1]+1}칸에서 가장 한산할 것으로 예상됩니다.'
                    
                    nr2 = self.table_an.rowCount()
                    self.table_an.setRowCount(nr2+3)
                    item_sen1 = QTableWidgetItem(sen1)
                    item_sen1.setBackground(QColor(76, 248, 106))
                    self.table_an.setItem(nr2,0,item_sen1)
                    self.table_an.setItem(nr2+1,0,QTableWidgetItem(sen2))
                    self.table_an.setItem(nr2+2,0,QTableWidgetItem(sen3))
                
            else:  
                if sum(nmean)==0: #혼잡도 내용이 다 0인 경우?
                
                    sen1 = f'{p_line.split()[0]} ({k1[h][0]} -> {k1[h][-1]})'
                    sen2 = f'혼잡도를 지원하지 않는 노선입니다.'
                    
                    nr2 = self.table_an.rowCount()
                    self.table_an.setRowCount(nr2+2)
                    item_sen1 = QTableWidgetItem(sen1)
                    item_sen1.setBackground(QColor(76, 248, 106))
                    self.table_an.setItem(nr2,0,item_sen1)
                    self.table_an.setItem(nr2+1,0,QTableWidgetItem(sen2))
          
                else:
                    ndif=[]
                    for i in range(len(nmean)-1):
                        sw=0
                        sw=nmean[i]-nmean[i+1]
                        ndif.append(sw)
            
                    w1=k1[h][nmean.index(max(nmean))] # 경로중 가장 사람 많은 역
                    w2=k1[h][ndif.index(max(ndif))] # 가장 사람이 많이 내리는 역
            
                    lii=k3[h]
                    list_data=[]
                    for j in lii:
                        li = [i for i in j if i!=0]
                        list_data.append(li)
                
                    column_sums = []
                    num_columns = len(list_data[0])  # 열의 개수를 구합니다.
        
                    for column_index in range(num_columns):
                        column_sum = sum(row[column_index] for row in list_data)
                        column_sums.append(column_sum)
                    
                    sorted_sums = sorted(column_sums)
                    
                    small_values = sorted_sums[:2]
                    large_values = sorted_sums[-2:]
                
                    if small_values[0] == small_values[1]:
                        small_values2 = list(filter(lambda x: column_sums[x] == small_values[0], range(len(column_sums))))
                    else:
                        small_values2 = [column_sums.index(value) for value in small_values]
                
                    if large_values[0] == large_values[1]:
                        large_values2 = list(filter(lambda x: column_sums[x] == large_values[0], range(len(column_sums))))
                    else:
                        large_values2 = [column_sums.index(value) for value in large_values]    
                
                    kk1=str(k1[h]).replace(',','->')
                    kk1=kk1.replace('[[','')
                    kk1=kk1.replace(']]','')
                    
                    sen1 = f'{p_line.split()[0]} ({k1[h][0]} -> {k1[h][-1]})'
                    sen2 = f'{large_values2[0]+1},{large_values2[1]+1}칸에서 가장 많은 혼잡이 예상되며, '
                    sen3 = f'{small_values2[0]+1},{small_values2[1]+1}칸에서 가장 한산할 것으로 예상됩니다.'
                    sen4 = f'{w1}을 지날 때 가장 혼잡할 것으로 예상되며, '
                    sen5 = f'{w2}을 지나면 여유공간이 확보될 것으로 예상됩니다.'

                    nr2 = self.table_an.rowCount()
                    self.table_an.setRowCount(nr2+5)
                    item_sen1 = QTableWidgetItem(sen1)
                    item_sen1.setBackground(QColor(76, 248, 106))
                    self.table_an.setItem(nr2,0,item_sen1)
                    self.table_an.setItem(nr2+1,0,QTableWidgetItem(sen2))
                    self.table_an.setItem(nr2+2,0,QTableWidgetItem(sen3))
                    self.table_an.setItem(nr2+3,0,QTableWidgetItem(sen4))
                    self.table_an.setItem(nr2+4,0,QTableWidgetItem(sen5))

    def buttonClicked_re2(self):
        self.close()
