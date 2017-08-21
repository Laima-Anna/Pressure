

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
from datetime import datetime,timedelta

import matplotlib.dates as mdates
from pathlib import Path

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import (QDialog,QWidget, QApplication, QVBoxLayout, QPushButton, QMenuBar, QMenu,
QAction,QFileDialog)

 

class BigWindow(QWidget):
    q=0
    allListsx=list()
    allListsy=list()
    xy=list()
    cv=list()
    diffTime=list() #keeps time values of difference
    diffY=list() #keeps y difference
    
    
    fileLoc=list() #keeps the names of selected files
    temper=list() #keeps temperature values
    meteoList= list() #keeps list of meteo data 
    
        
        
    def __init__(self, parent=None):
        super(BigWindow, self).__init__(parent)

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
                    #print(my_list1[val][0])
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
                   
                    if len(num3)==1:
                        num31="0"+str(num3)
                        
                    my_list1[val][5]=num0
                    my_list1[val][4]=num7
                    my_list1[val][3]=num6
                    my_list1[val][2]=num4
                    my_list1[val][1]=num31
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
        
            
            
        if len(self.allListsx)>1:
            self.getSimVal()
            self.yDiff()
    
       
        self.openSmallMain()
        
        
    def splitVal(self, lis,i):
        #splits two vales seperated by comma
        x=[]
        y=[]
        
        
        for j in range(0,len(lis[i])):
            val1=lis[i][j]
            val = val1.split(',')
            x.append(val[0])
            y.append(val[1])
        
        return x,y
    
    def yDiff(self):
        
        
        
        #if you have selected more than one file
        if len(self.fileLoc)>1:
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
            
            #splits the values and append them to arrays
            for i in range(0,len(self.xy)):
            
                x4,y4=self.splitVal(self.xy,i)
                c4,v4=self.splitVal(self.cv,i)
                x6.append(x4)
                y6.append(y4)
                c6.append(c4)
                v6.append(v4)
            
            #changes every value to int and puts them into numpy array
            x = np.array([int(i) for i in x4])
            y = np.array([int(i) for i in y4])
            c = np.array([int(i) for i in c4])
            v = np.array([int(i) for i in v4])
    
            #sets the beginning value
            u=x[0]
            #gets value for every second
            for u in range (x[0],x[-1]):
                x5.append(u)
                y5.append(np.interp(u, x, y))
              
            u1=c[0]
            for u1 in range (c[0],c[-1]):
                c5.append(u1)
                v5.append(np.interp(u1, c, v))  
            
            #compares if the beginning of two files is the same, if not then deletes them
            for r in range (0,10):
                if x5[0]!=c5[0]:
                    if x5[0]<c5[0]:
                        del x5[0]
                        del y5[0]
                    if x5[0]>c5[0]:
                        del c5[0]
                        del v5[0]
            
            #compares if the end of two files is the same, if not then deletes them
            for r1 in range (0,10):
                if x5[-1]!=c5[-1]:
                    if x5[-1]>c5[-1]:
                        del x5[-1]
                        del y5[-1]
                    if x5[-1]<c5[-1]:
                        del c5[-1]
                        del v5[-1]
         
            #changes to numpy array
            y1=np.array(y5)
            v1=np.array(v5)
            
           
            #checks if the file exists already
            for i in range (1,100):
                my_file = Path("yValues%i.txt"%i)
                if my_file.is_file():
                    pass
                else:
                    fileNam="yValues%i.txt"%i
                    break
            
            
            #writes time and difference into file
            with open(fileNam,'w',encoding = 'utf-8') as thefile:
                if (y1[0]>v1[0]):
                    #substracts two values
                    diff=np.subtract(y1,v1)
                    
                    #writes into a file and appends to arrays
                    for i in range(0,len(diff)):
                        time=self.GetTime(x5[i])         
                        diff2="%.1f" % round(diff[i],2)
                        thefile.write(str(time)+","+str(diff2))
                        thefile.write("\n")
                        self.diffTime.append(time)
                        self.diffY.append(diff2)
                else:
                    diff=np.subtract(v1,y1)
                    
                    for i in range(0,len(diff)):
                        time=self.GetTime(x5[i])
                        diff2="%.1f" % round(diff[i],2)
                        thefile.write(str(time)+","+str(diff2))
                        thefile.write("\n")
                        self.diffTime.append(time)
                        self.diffY.append(diff2)
        
        
        
    def openSmallMain(self):
        
        #import SmallMain
        #self.dialog_04 = SmallMain.SmallWindow()
        self.dialog_04 = SmallWindow()
        self.dialog_04.show()
        self.dialog_04.raise_()
        
    
   
    
    
    def GetTime(self,x):  
        #changes seconds to date
        sec = timedelta(minutes=x)
        d1=str(datetime(2017,1,1) + sec)
        d1 = d1[:-3]
        return d1
        
        
      
            
    def getSimVal(self):
        
        x2=0
        c2=0
        listxy=list()
        listcv=list()
        
        #goes through first two lists in allListsx (y) and compares if the date in seconds is the same 
        if len(self.allListsx)>1:
            
            x=self.allListsx[0]
            c=self.allListsx[1]
            y=self.allListsy[0]
            v=self.allListsy[1]
                  
            for i in range(0,len(x)-1):
                x1=x[i]
                y1=y[i]
                for j in range(0,len(c)-1):
                    c1=c[j]
                    v1=v[j]
                    if (x1-5)<=c1<=(x1+5):
                        if(c1!=c2):
                            listcv.append(str(c1)+","+str(v1))
                            #print(str(c1)+","+str(v1))
                            c2=c1
                        if(x1!=x2):
                            listxy.append(str(x1)+","+str(y1))
                            #print(str(x1)+","+str(y1))
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





        
    
class OpenFinalDialog(QDialog):
    
    
    def __init__(self, parent=None):
        super(OpenFinalDialog, self).__init__(parent)
        
        self.resize(1000,600)
        self.move(900,500)
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        
        
        
        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)      
        
        self.plot1()
    
    def convertTemp(self):
        x1=SmallWindow.finalDateTemp
        y=SmallWindow.finalTemp
        x=[]
        x2=list()
        y2=list()
        x3=list()
        
        for i in range(len(x1)):
            s2 = x1[i]
            #fmt = '%Y/%m/%d %H:%M'
            d1 = datetime(2017,1,1)
            #d2 = datetime.strptime(s2, fmt)
            d3 = (s2-d1)
            d4=d3.days, d3.seconds//3600, (d3.seconds//60)%60
            d5=d4[0]*24*60+d4[1]*60+d4[2]
            x.append(d5)
       
        #sets the beginning value
        u=x[0]
        #gets value for every second
        for u in range (x[0],x[-1]):
            x2.append(u)
            y2.append(np.interp(u, x, y))
        
        for i in range(0, len(x2)):
            sec = timedelta(minutes=x2[i])
            d1=datetime(2017,1,1) + sec
            x3.append(d1)
            
        return x3,y2
        
    def plot1(self):
        x = []
        y = []
        x1=[]
        y1=[]
        finalx=[]
        finaly=[]
        
        
        x1=SmallWindow.finalDateDiff
        y1=SmallWindow.finalDiff
        x,y=self.convertTemp()
        
        
        for i in range(0,len(x)):
            for j in range(0,len(x1)):
                if x[i]==x1[j]:
                    finalx.append(y[i])
                    finaly.append(y1[j])
                    
                    
        
        ax = self.figure.add_subplot(111)
        ax.plot(finalx, finaly,"o")  
        
        finalx = [float(i) for i in finalx]
        finaly = [float(i) for i in finaly]
        
        ar=np.array(finalx)
        at=np.array(finaly)
        
        ax.plot(ar, np.poly1d(np.polyfit(ar, at, 1))(ar))
        
        # refresh canvas
        self.canvas.draw()
        
     
   
        
        
class SmallWindow(QDialog):
    q=0
    finalDateDiff=list()
    finalDateTemp=list()
    finalDiff=list()
    finalTemp=list()
    
    def __init__(self, parent=None):
        super(SmallWindow, self).__init__(parent)
        
        self.resize(1000,600)
        self.move(900,0)
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)


        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
       
        self.setLayout(layout)
        
        self.plot1()

    
    def plot1(self):
        colors=['b','g','r','c','m','y','k']
        colLen=len(colors)
        #clear graphs
        #self.figure.clear()
        
        for o in range(0,len(BigWindow.fileLoc)):
            if self.q>=colLen-1:
                self.q=0
                #print(self.q)
            else:
                self.q=self.q+1
                #print(self.q)
           
                
            self.plot(colors[self.q],o) 
            
    
            
        
        
        self.openFinal()
        
    def plot(self,color,o):
        y = []
        t = []
        

        
        if "M" in BigWindow.fileLoc[o]:
            readFile = open(BigWindow.fileLoc[o], 'r')
            sepFile = readFile.read().split('\n')
            readFile.close()
            for idx, plotPair in enumerate(sepFile):
                if plotPair in '. ':
                    # skip. or space
                    continue
                if idx >= 0:  
                
                    every = plotPair.split(' ')
                    time_string = str(every[0])+str("-")+str(every[1])+str("-")+str(every[2])+str(" ")+str(every[3])+str(":")+str(every[4])
                    time_string1 = datetime.strptime(time_string, '%Y-%m-%d %H:%M')
                    t.append(time_string1)
                    y.append(float(every[6]))
                    self.finalDateTemp.append(time_string1)
                    self.finalTemp.append(float(every[6]))
        else:
            t=BigWindow.diffTime
            y=BigWindow.diffY
            for i in range (0,len(t)):
                a=t[i]
                time_string1 = datetime.strptime(a, '%Y-%m-%d %H:%M')
                t[i]=time_string1
                self.finalDateDiff.append(time_string1)
                self.finalDiff.append(y[i])
 

        ax = self.figure.add_subplot(111)
        self.figure.autofmt_xdate(rotation=45)
        ax.plot(t, y, color)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y %H:%M'))
        # refresh canvas
        self.canvas.draw()
        
        
    def openFinal(self):
        self.dialog_03 = OpenFinalDialog()
        self.dialog_03.show()
        self.dialog_03.raise_()

    
    
    
        
        
        
    
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
 
    main = BigWindow()
    main.setWindowTitle('Pressure data')
    main.show()
 
    sys.exit(app.exec_())
    
    
    
    