import sys
import numpy as np
from PyQt5.QtWidgets import (QDialog, QApplication, QPushButton, QVBoxLayout, QMenuBar,
QMainWindow,QMenu,QAction,QTextEdit,QFileDialog)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from PyQt5.QtGui import QIcon
from datetime import datetime, timedelta
import matplotlib.dates as mdates

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

        
        
        self.plot1()

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)      
    
    def plot1(self):
        y = []
        t = []
        
        #name=OpenDialog.fileLoc[0]
        readFile = open("finalDateDiffTemp.txt", 'r')
        sepFile = readFile.read().split('\n')
        readFile.close()
        for idx, plotPair in enumerate(sepFile):
            if plotPair in '. ':
                # skip. or space
                continue
            if idx >= 0:  
                xAndY = plotPair.split(',') 
                t.append(xAndY[2])
                y.append(xAndY[1])
                   


        ax = self.figure.add_subplot(111)
        ax.plot(t, y,"o")  
        
        y = [float(i) for i in y]
        t = [float(i) for i in t]
        
        ar=np.array(t)
        at=np.array(y)
        
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
        
        for i in range(0,1):
            if self.q>=colLen-1:
                self.q=0
                #print(self.q)
            else:
                self.q=self.q+1
                #print(self.q)
           
            self.plot(colors[self.q]) 
            
    
            
        
        
        #self.openFinal()
        
    def plot(self,color):
        y = []
        t = []
        
        import PressureProg
        #BigWin=PressureProg.BigWindow()
        t,y=PressureProg.BigWindow().getDiffArrays()
        
        
        print(t)
        print(y)
        """
        readFile = open(name, 'r')
        sepFile = readFile.read().split('\n')
        readFile.close()
        for idx, plotPair in enumerate(sepFile):
            if plotPair in '. ':
                # skip. or space
                continue
            if idx >= 0:  
                if "temperM" in label1:
                    xAndY = plotPair.split(',')
                    time_string = xAndY[0]
                    time_string1 = datetime.strptime(time_string, '%Y/%m/%d %H:%M')
                    t.append(time_string1)
                    y.append(float(xAndY[1]))
                    self.finalDateTemp.append(time_string1)
                    self.finalTemp.append(float(xAndY[1]))
                else:
                    xAndY = plotPair.split(',')
                    time_string = xAndY[0]
                    sec = timedelta(minutes=int(time_string))
                    d1 = datetime(2017,1,1)+sec
                    #time_string1 = datetime.strptime(d1, '%Y-%m-%d %H:%M')
                    t.append(d1)
                    y.append(float(xAndY[1]))
                    self.finalDateDiff.append(d1)
                    self.finalDiff.append(float(xAndY[1]))
        
        """

        ax = self.figure.add_subplot(111)
        #self.figure.autofmt_xdate(rotation=45)
        ax.plot(t, y, color)
        #ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y %H:%M'))
        # refresh canvas
        self.canvas.draw()
        
        
    def openFinal(self):
        self.dialog_03 = OpenFinalDialog()
        self.dialog_03.show()
        self.dialog_03.raise_()
