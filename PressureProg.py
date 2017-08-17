

"""
Created on Thu Dec 12 08:38:21 2013
 
@author: Sukhbinder Singh
 
Simple QTpy and MatplotLib example with Zoom/Pan
 
Built on the example provided at
How to embed matplotib in pyqt - for Dummies
http://stackoverflow.com/questions/12459811/how-to-embed-matplotib-in-pyqt-for-dummies
 
"""
import sys, os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

import matplotlib.dates as mdates
from pathlib import Path

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout, QPushButton, QMenuBar, QMenu,
QAction,QFileDialog)

 

class Window(QWidget):
    q=0
    allListsx=list()
    allListsy=list()
    xy=list()
    cv=list()
    
    
    
    fileLoc=list() #keeps the names of selected files
    temper=list() #keeps temperature values
    meteoList= list() #keeps list of meteo data 
    
        
        
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
 
        self.resize(1300,800)
        self.move(0,100)
       
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        
        self.menuBar = QMenuBar(self)
        self.menuOpen = QMenu("File", self.menuBar)
        self.actionOpen = QAction('Open', self)
        self.actionOpen.triggered.connect(self.open_clicked)
        self.actionQuit = QAction('Quit', self)
        self.actionQuit.triggered.connect(self.close)
        
        self.menuOpen.addAction(self.actionOpen)
        self.menuOpen.addAction(self.actionQuit)
        self.menuBar.addAction(self.menuOpen.menuAction())
        

        # Just some button 
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plotOrigin)
        self.button1 = QPushButton('Reset')
        self.button1.clicked.connect(self.resetA)
 
        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)
 
    
    def open_clicked(self):
        
        #opens file explorer
        fname = QFileDialog.getOpenFileNames(self, 'Open file', '/home')
        fname1=fname[0]
        #appends file names to fileLocation list and text window
        for e in range(0,len(fname1)):#varbūt šo nevajag ja izmanto vienā vietā
            self.fileLoc.append(fname1[e])#šo arī
            

     
        #open all selected files 
        for i in range(0,len(self.fileLoc)):
            #to check the name of file
            file=self.fileLoc[i]
            fileName=file.split('/')
            fileName1=fileName[-1]
            #i=i+1
            #to open and read M file
            if "M" in fileName1:
                f = open(fileName1, 'r')
                my_list = [line.split(' ') for line in f.readlines()]
                f.close()
                
                #to put in list temperature values
                for i in range(0,len(my_list)):
                    date=str(my_list[i][0])+"/"+str(my_list[i][1])+"/"+str(my_list[i][2])+" "+str(my_list[i][3])+":"+str(my_list[i][4])
                    dat=my_list[i][-3]  
                    self.temper.append(str(date)+","+str(dat)+"\n")
                    
                
                #take the right value and calculate it to pascals 
                for val in range(0,len(my_list)):
    
                    data=float(my_list[val][-1])
                    data2=str(int(data*133.322387415))
                    my_list[val][5]=data2
                    del my_list[val][6:9]
                    
                
                #append meteo data from one file to global list
                self.meteoList.append(my_list)
                       
            #to read slr meteo files
            else:
                f = open(fileName1, 'r') #var uztaisit def
                my_list1 = [line.split(' ') for line in f.readlines()]
                f.close()
                
                #take the right value calculate it to pascals, move to right places
                for val in range(0,len(my_list1)):
    
                    data=float(my_list1[val][0])
                    data2=str(int(data*100))
                    my_list1[val][0]=data2

                    last=my_list1[val][-1]
                    last1=last.strip()
                    my_list1[val][-1]=last1

                    num0=my_list1[val][0]
                    num2=my_list1[val][2]
                    num3=my_list1[val][3]
                    num4=my_list1[val][4]
                    num6=my_list1[val][6]
                    num7=my_list1[val][7]
                    my_list1[val][5]=num0
                    my_list1[val][4]=num7
                    my_list1[val][3]=num6
                    my_list1[val][2]=num4
                    my_list1[val][1]=num3
                    my_list1[val][0]=num2
                    del my_list1[val][6:8]
               
                self.meteoList.append(my_list1)

        #print(self.meteoList)
        #print("----")
        #print(self.slrList)
    
    def resetA(self):
        #Add all things that need to be reseted
        
        return
    
    
    def plotOne(self,color,label1,i):
        y = []
        t = []
        
        #takes everything from meteoList and convert to right format
        for idx in range(0,len(self.meteoList[i])):
                time_string = str(self.meteoList[i][idx][0])+"/"+str(self.meteoList[i][idx][1])+"/"+str(self.meteoList[i][idx][2])+" "+str(self.meteoList[i][idx][3])+":"+str(self.meteoList[i][idx][4])
                time_string1 = datetime.strptime(time_string, '%Y/%m/%d %H:%M')
                t.append(time_string1)
                y.append(float(self.meteoList[i][idx][5]))
                    
        self.ax = self.figure.add_subplot(111)
        self.figure.autofmt_xdate(rotation=45)
        
        self.ax.plot(t, y, color, label=label1)
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y %H:%M'))
        self.ax.set_ylabel('Pressure (Pa)', fontSize=16)
        
        
        self.canvas.draw()
    
   
        
    def plotOrigin(self):
        
        
        import SmallMain
        #small = SmallMain.Window()
        self.dialog_04 = SmallMain.Window()
        self.dialog_04.show()
        self.dialog_04.raise_()
        
        #generate some graph colors
        colors=['b','g','r','c','m','y','k']
      
        #plot all data in meteoList
        for i in range(0,len(self.fileLoc)):
            if self.q>=(len(colors)):
                self.q=0
                
            else:
                self.q=self.q+1
            
            #get file name for label
            file=self.fileLoc[i]
            fileName=file.split('/')
            fileName1=fileName[-1]
            
            #call a function that plots everythong one by one
            self.plotOne(colors[self.q],fileName1,i) 
   
            #get vales from changeToSec
            x,y=self.changeToSec(i)
            #put new data into lists
            self.allListsx.append(x)
            self.allListsy.append(y)
        
            
            
            
        self.getSimVal()
        self.yDiff()
    
    def splitVal(self, lis,i):
        x=[]
        y=[]
        
        
        for j in range(0,len(lis[i])):
            val1=lis[i][j]
            val = val1.split(',')
            x.append(val[0])
            y.append(val[1])
        
        return x,y
    
    def yDiff(self):
        x4=[]
        y4=[]
        c4=[]
        v4=[]
        x5=[]
        y5=[]
        c5=[]
        v5=[]
        x6=[]
        y6=[]
        c6=[]
        v6=[]
        
        for i in range(0,len(self.xy)):
        
            x4,y4=self.splitVal(self.xy,i)
            c4,v4=self.splitVal(self.cv,i)
            x6.append(x4)
            y6.append(y4)
            c6.append(c4)
            v6.append(v4)
            
        print(len(x6))
        print("-----")
        #neraksta pareizās atšķirības failā
        
        x4 = [int(i) for i in x4]
        y4 = [int(i) for i in y4]
        c4 = [int(i) for i in c4]
        v4 = [int(i) for i in v4]
        
        x = np.array(x4)
        y = np.array(y4)
        c = np.array(c4)
        v = np.array(v4)

        
        u=x4[0]
        for u in range (x4[0],x4[-1]):
            x5.append(u)
            y5.append(np.interp(u, x, y))
          
        u1=c4[0]
        for u1 in range (c4[0],c4[-1]):
            c5.append(u1)
            v5.append(np.interp(u1, c, v))  
        

        for r in range (0,10):
            if x5[0]!=c5[0]:
                if x5[0]<c5[0]:
                    del x5[0]
                    del y5[0]
                if x5[0]>c5[0]:
                    del c5[0]
                    del v5[0]
        
        
        for r in range (0,10):
            if x5[-1]!=c5[-1]:
                if x5[-1]>c5[-1]:
                    del x5[-1]
                    del y5[-1]
                if x5[-1]<c5[-1]:
                    del c5[-1]
                    del v5[-1]
     
        y1=np.array(y5)
        v1=np.array(v5)
        
       
        
                    
        
        for i in range (1,100):
            my_file = Path("yValues%i.txt"%i)
            if my_file.is_file():
                pass
            else:
                fileNam="yValues%i.txt"%i
                break

        
        with open(fileNam,'w',encoding = 'utf-8') as thefile:
            if (y1[0]>v1[0]):
                diff=np.subtract(y1,v1)
                
                for i in range(0,len(diff)):
                    diff2="%.1f" % round(diff[i],2)
                    thefile.write(str(x5[i])+","+str(diff2))
                    thefile.write("\n")
            else:
                diff=np.subtract(v1,y1)
                
                for i in range(0,len(diff)):
                    diff2="%.1f" % round(diff[i],2)
                    thefile.write(str(x5[i])+","+str(diff2))
                    thefile.write("\n")
        
        #return
        
        
    def getSimVal(self):
        
        x2=0
        c2=0
        listxy=list()
        listcv=list()
        
        #goes through every list in allListsx (y) and compares if the date in seconds is the same 
        if len(self.allListsx)>1:
            for ze in range(0,len(self.allListsx)):
                for zr in range(0,len(self.allListsx)):
                    print(len(self.allListsx))
                    
                    if ze+zr<len(self.allListsx):
                       
                        x=self.allListsx[ze]
                        c=self.allListsx[ze+zr]
                        y=self.allListsy[ze]
                        v=self.allListsy[ze+zr]
                        for i in range(0,len(x)-1):
                            x1=x[i]
                            y1=y[i]
                            for j in range(0,len(c)-1):
                                c1=c[j]
                                v1=v[j]
                                if (x1-5)<=c1<=(x1+5):
                                    if(c1!=c2):
                                        listcv.append(str(c1)+","+str(v1))
                                        c2=c1
                                    if(x1!=x2):
                                        listxy.append(str(x1)+","+str(y1))
                                        x2=x1
                                
                    self.cv.append(listcv)
                    self.xy.append(listxy)
        
    def changeToSec(self,i):
        
        h=[]
        z=[]
        y=[]
        
        #takes everything from meteoList and convert to right format
        for idx in range(0,len(self.meteoList[i])):
                time_string = str(self.meteoList[i][idx][0])+"/"+str(self.meteoList[i][idx][1])+"/"+str(self.meteoList[i][idx][2])+" "+str(self.meteoList[i][idx][3])+":"+str(self.meteoList[i][idx][4])
                z.append(time_string)
                y.append(float(self.meteoList[i][idx][5]))
     
        #convert every date into seconds from 01.01.2017
        for i in range(len(z)):
            s2 = z[i]
            fmt = '%Y/%m/%d %H:%M'
            d1 = datetime(2017,1,1)
            d2 = datetime.strptime(s2, fmt)
            d3 = (d2-d1)
            d4=d3.days, d3.seconds//3600, (d3.seconds//60)%60
            d5=d4[0]*24*60+d4[1]*60+d4[2]
            h.append(d5)
            
        #changes every y value to type int
        y = [int(i) for i in y]
        
        return h,y


        
    

    
    
    
        
        
        
    
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
 
    main = Window()
    main.setWindowTitle('Pressure data')
    main.show()
 
    sys.exit(app.exec_())