import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from app.menu import menu
from app.appContent import appContent
from audio import audioHandler

class Suppressor(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        self.audioPath = ''
        
        
    def initUI(self):               
        exitAct = self.exitAction()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu(' &File')
        fileMenu.addAction(exitAct)

        self.statusBar()

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        grid = QGridLayout(centralWidget)
        centralWidget.setLayout(grid)

        self.mountBoxes(grid)

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Acoustic noise suppresion')    
        self.show()

    def exitAction(self):
        exitAct = QAction(' &Exit', self)
        exitAct.triggered.connect(qApp.quit)

        return exitAct      
        
    def mountBoxes(self, contentGrid):
        specSubGroup = appContent.spectralSubtractionBox()
        flmsGroup = appContent.fastLMSBox()
        plcaGroup = appContent.plcaBox()
        runGroup = appContent.runBox(self)

        contentGrid.addWidget(specSubGroup, 0, 0, 2, 2)
        contentGrid.addWidget(flmsGroup, 0, 2, 2 , 2)
        contentGrid.addWidget(plcaGroup, 0, 4, 2, 2)
        contentGrid.addWidget(runGroup, 2, 0, 1, 6)
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    suppressor = Suppressor()
    sys.exit(app.exec_())
