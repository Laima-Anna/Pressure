

"""
Created on Thu Dec 12 08:38:21 2013
 
@author: Sukhbinder Singh
 
Simple QTpy and MatplotLib example with Zoom/Pan
 
Built on the example provided at
How to embed matplotib in pyqt - for Dummies
http://stackoverflow.com/questions/12459811/how-to-embed-matplotib-in-pyqt-for-dummies
 
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

import matplotlib.dates as mdates
from pathlib import Path

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout, QPushButton, QMenuBar, QMenu,
QAction,QMainWindow, QFileDialog,QTextEdit)
from PyQt5.QtGui import QIcon


class OpenDialog(QMainWindow):
        
    fileLoc=list()
    fileLoc1=list()
    z=0
    temper=list()
   
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):      
        
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()
        
       
        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)
        
        done = QAction( 'Done', self)
        done.setShortcut('Ctrl+D')
        done.setStatusTip('Done and close')
        done.triggered.connect(self.close)
        done.triggered.connect(self.done)
        #done.triggered.connect(self.interpol)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)    
        fileMenu.addAction(done)
       
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()

   
        
    def showDialog(self):
       
        fname = QFileDialog.getOpenFileNames(self, 'Open file', '/home')
        fname1=fname[0]
        leng1=len(fname1)
        e=0
        for e in range(0,leng1):
            name=fname1[e]
            self.textEdit.append(name)
            self.fileLoc.append(name)
            self.fileLoc1.append(name)
            e=e+1
    


    def done(self):
        #print(self.fileLoc)
        
        for i in range(0,len(self.fileLoc)):
            file=self.fileLoc[i]
            fileName=file.split('/')
            fileName1=fileName[-1]
            i=i+1
            if "M" in fileName1:
                f = open(fileName1, 'r')
                my_list = [line.split(' ') for line in f.readlines()]
                f.close()
                
               
                with open("temper"+fileName1,'w',encoding = 'utf-8') as thefile:
                    for i in range(0,len(my_list)):
                        date=str(my_list[i][0])+"/"+str(my_list[i][1])+"/"+str(my_list[i][2])+" "+str(my_list[i][3])+":"+str(my_list[i][4])
                       
                        dat=my_list[i][-3]  
                        thefile.write(str(date))
                        thefile.write(',')
                        thefile.write(str(dat))
                        thefile.write("\n")
                    
                    
                    
                for val in range(0,len(my_list)):
    
                    data=my_list[val][-1]
                    data1=float(data)
                    data2=data1*133.322387415
                    data3=int(data2)
                    data4=str(data3)
                    my_list[val][5]=data4
                    del my_list[val][6:8]

                print(self.temper)  

                
                numbers2=list(range(0,len(my_list)))
                
                file1=str("Meteo")+str(fileName1)
                self.writeFile(file1,numbers2,my_list)
                
                
            else:
                f = open(fileName1, 'r')
                my_list1 = [line.split(' ') for line in f.readlines()]
                f.close()
                lenght=len(my_list1)
                numbers=list(range(0,lenght))
                #numbers1=[0,2,3,4,6,7]
                for val in numbers:
    
                    data=my_list1[val][0]
                    data1=float(data)
                    data2=data1*100
                    data3=int(data2)
                    data4=str(data3)
                    my_list1[val][0]=data4

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
                
                file1=str("SLR")+str(fileName1)
                self.writeFile(file1,numbers,my_list1)
                
    
    
    
    def writeFile(self,file,numbers,my_list):
        
        with open(file,'w',encoding = 'utf-8') as thefile:
            for val in numbers:
                thefile.write(my_list[val][0])
                thefile.write('/')
                thefile.write(my_list[val][1])
                thefile.write('/')
                thefile.write(my_list[val][2])
                thefile.write(' ')
                thefile.write(my_list[val][3])
                thefile.write(':')
                thefile.write(my_list[val][4])
                thefile.write(',')
                thefile.write(my_list[val][5])
                thefile.write("\n")
        
       # leng=len(self.fileLoc)
       # for i in range(0,leng):
        
        
        fileNa=self.fileLoc[self.z]
        fileName=fileNa.split('/')
        fileName[-1]=file 
        fileName2='/'.join(fileName)
        self.fileLoc1[self.z]=fileName2
        
       # print(self.fileLoc)
            
        self.z=self.z+1
        


class Window(QWidget):
    q=0
    allListsx=list()
    allListsy=list()
    xyes=list()
    cyes=list()
    yyes=list()
    zyes=list()
    
    def open_clicked(self):
        self.dialog_02 = OpenDialog()
        self.dialog_02.show()
        self.dialog_02.raise_()
        

        
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
 
        self.resize(1300,900)
         
       
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
        self.button.clicked.connect(self.plott)
 
        #self.button1 = QPushButton('Reset')
        #self.button1.clicked.connect(self.reset)
         
        #self.button2 = QPushButton('Pan')
        #self.button2.clicked.connect(self.pan)
         
        #self.button3 = QPushButton('Home')
       # self.button3.clicked.connect(self.home)
        
 
        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        #layout.addWidget(self.button1)
        #layout.addWidget(self.button2)
        #layout.addWidget(self.button3)
        self.setLayout(layout)
 
    #def reset(self):
        
    
        
        #self.figure.clf()
        
        
    #def zoom(self):
     #   self.toolbar.zoom()
    #def pan(self):
     #   self.toolbar.pan()
    
    def plot1(self,name,color,label1):
        
        y = []
        t = []
        readFile = open(name, 'r')
        sepFile = readFile.read().split('\n')
        readFile.close()
        for idx, plotPair in enumerate(sepFile):
            if plotPair in '. ':
                # skip. or space
                continue
            if idx >= 0:  
                xAndY = plotPair.split(',')
                time_string = xAndY[0]
                time_string1 = datetime.strptime(time_string, '%Y/%m/%d %H:%M')
                t.append(time_string1)
                y.append(float(xAndY[1]))
    
        self.ax = self.figure.add_subplot(111)
        self.figure.autofmt_xdate(rotation=45)
        
        self.ax.plot(t, y, color, label=label1)
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y %H:%M'))
        self.ax.set_ylabel('Pressure (Pa)', fontSize=16)
        #first_legend = plt.legend( loc=2,prop={'size':18})
        #self.ax = plt.gca().add_artist(first_legend)
        
        self.canvas.draw()
        
        
    def plott(self):
        
        colors=['b','g','r','c','m','y','k']
        colLen=len(colors)
        colLen1=colLen-1
        
        leng=len(OpenDialog.fileLoc1)
        #print(leng)
        for i in range(0,leng):
            if self.q>=colLen1:
                self.q=0
                #print(self.q)
            else:
                self.q=self.q+1
                #print(self.q)
            file=OpenDialog.fileLoc1[i]
            fileName=file.split('/')
            fileName1=fileName[-1]
            self.plot1(file,colors[self.q],fileName1) 
            
            x,y=self.interpol(file)
            self.allListsx.append(x)
            self.allListsy.append(y)
        
            
            
            i=i+1
        self.xycv()
        self.yDiff()
            #os.remove(file)
            
    def yDiff(self):
        x4=[]
        y4=[]
        c4=[]
        v4=[]
        x5=[]
        y5=[]
        c5=[]
        v5=[]
        
        
        readFile = open("xany.txt", 'r')
        sepFile = readFile.read().split('\n')
        readFile.close()
        for idx, plotPair in enumerate(sepFile):
            if plotPair in '. ':
                # skip. or space
                continue
            if idx >= 0:  
                xAndY = plotPair.split(',')
                x3 = xAndY[0]
                y3= xAndY[1]
                x4.append(x3)
                y4.append(y3)
        
        readFile = open("canv.txt", 'r')
        sepFile = readFile.read().split('\n')
        readFile.close()
        for idx, plotPair in enumerate(sepFile):
            if plotPair in '. ':
                # skip. or space
                continue
            if idx >= 0:  
                xAndY = plotPair.split(',')
                c3 = xAndY[0]
                v3= xAndY[1]
                c4.append(c3)
                v4.append(v3)     
  
        
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

    
    def xycv(self):
        ze=0
        x2=0
        c2=0
        with open("xany.txt",'w',encoding = 'utf-8') as filexy, open("canv.txt",'w',encoding = 'utf-8') as filecv:
            if len(self.allListsx)>1:
                for ze in range(0,len(self.allListsx)-1):
                    x=self.allListsx[ze]
                    c=self.allListsx[ze+1]
                    y=self.allListsy[ze]
                    v=self.allListsy[ze+1]
                    #print(self.allListsx)
                    #print(c)
                    for i in range(0,len(x)-1):
                        x1=x[i]
                        y1=y[i]
                        #print(str(x[i])+"x-"+str(i))
                        for j in range(0,len(c)-1):
                            c1=c[j]
                            v1=v[j]
                            #print(str(c[i])+"c-"+str(i))
                            if (x1-5)<=c1<=(x1+5):
                                if(c1!=c2):
                                    filecv.write(str(c1)+","+str(v1))
                                    filecv.write("\n")
                                    c2=c1
                                if(x1!=x2):
                                    filexy.write(str(x1)+","+str(y1))
                                    filexy.write("\n")
                                    x2=x1
                                        
                                #print("Yes")
                                #print(x1)
                                #print(c1)
                                #self.cyes.append(j)
                                #self.xyes.append(i) 
                        j=j+1
                    
            
                    i=i+1
    
        
        
        
    def interpol(self,file):
        
        #import numpy as np
        from datetime import datetime
        #from scipy.interpolate import splrep, splev
        #print(file)
        h=[]
        z=[]
        y = []
        

     
        readFile = open(file, 'r')
        sepFile = readFile.read().split('\n')
        readFile.close()
        #print(sepFile)
        for idx, plotPair in enumerate(sepFile):
            if plotPair in '. ':
                # skip. or space
                continue
            if idx >= 0:  
                xAndY = plotPair.split(',')
                time_string = xAndY[0]
                z.append(time_string)    
                y.append(xAndY[1])
                


        for i in range(len(z)):
            s2 = z[i]
            fmt = '%Y/%m/%d %H:%M'
            d1 = datetime(2017,1,1)
            d2 = datetime.strptime(s2, fmt)
            d3 = (d2-d1)
            d4=d3.days, d3.seconds//3600, (d3.seconds//60)%60
            d5=d4[0]*24*60+d4[1]*60+d4[2]
            h.append(d5)
            

        y = [int(i) for i in y]
        #x = np.array(h)
        #y = np.array(y)
        

        #print (np.interp(266872, x, y))
        #tck = splrep(x, y)
        #print(splev(266872, tck))
        return h,y
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
 
    main = Window()
    main.setWindowTitle('Pressure data')
    main.show()
 
    sys.exit(app.exec_())