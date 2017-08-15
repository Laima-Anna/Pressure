import sys, os
from PyQt5.QtWidgets import (QDialog, QApplication, QPushButton, QVBoxLayout, QMenuBar,
QMainWindow,QMenu,QAction,QTextEdit,QFileDialog)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from PyQt5.QtGui import QIcon
from datetime import datetime, timedelta
import matplotlib.dates as mdates

class OpenDialog(QMainWindow):
        
    fileLoc=list()
    fileLoc1=list()
    z=0
   
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
        #done.triggered.connect(self.done)
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
            #self.fileLoc1.append(name)
            e=e+1


        
        
        
class Window(QDialog):
    q=0
    
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        
        self.resize(1300,900)
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
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
        
        
        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot1)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    
    def open_clicked(self):
        self.dialog_02 = OpenDialog()
        self.dialog_02.show()
        self.dialog_02.raise_()
    
    
    def plot1(self):
        colors=['b','g','r','c','m','y','k']
        colLen=len(colors)
        #clear graphs
        #self.figure.clear()
       
        for i in range(0,len(OpenDialog.fileLoc)):
            if self.q>=colLen-1:
                self.q=0
                #print(self.q)
            else:
                self.q=self.q+1
                #print(self.q)
            file=OpenDialog.fileLoc[i]
            
            fileName=file.split('/')
            fileName1=fileName[-1]
            self.plot(file,colors[self.q],fileName1) 
            
    
            i=i+1
    
    def plot(self,name,color,label1):
        y = []
        t = []
        
        #name=OpenDialog.fileLoc[0]
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
                else:
                    xAndY = plotPair.split(',')
                    time_string = xAndY[0]
                    sec = timedelta(minutes=int(time_string))
                    d1 = datetime(2017,1,1)+sec
                    #time_string1 = datetime.strptime(d1, '%Y-%m-%d %H:%M')
                    t.append(d1)
                    y.append(float(xAndY[1]))
        
     

        ax = self.figure.add_subplot(111)
        self.figure.autofmt_xdate(rotation=45)
        ax.plot(t, y, color, label=label1)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y %H:%M'))
        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())