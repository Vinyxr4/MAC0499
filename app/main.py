import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QAction, qApp, QGroupBox, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon
from app.menu import menu

class Suppressor(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):               
        # exitAct = self.exitAction()

        # menubar = self.menuBar()
        # fileMenu = menubar.addMenu(' &File')
        # fileMenu.addAction(exitAct)

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
        specSubGroup = self.spectralSubtractionBox()
        flmsGroup = self.fastLMSBox()
        plcaGroup = self.plcaBox()
        runGroup = self.runBox()

        contentGrid.addWidget(specSubGroup, 0, 0, 2, 2)
        contentGrid.addWidget(flmsGroup, 0, 2, 2 , 2)
        contentGrid.addWidget(plcaGroup, 0, 4, 2, 2)
        contentGrid.addWidget(runGroup, 2, 0, 1, 6)

    def spectralSubtractionBox(self):
        specSubGroup = QGroupBox('Spectral Subtraction')
        specSubLayout = QVBoxLayout()

        specSubLayout.addWidget(QPushButton('test'))
        specSubGroup.setLayout(specSubLayout)

        return specSubGroup
        
    def fastLMSBox(self):
        flmsGroup = QGroupBox('Fast LMS')
        flmsLayout = QVBoxLayout()

        flmsLayout.addWidget(QPushButton('test'))
        flmsGroup.setLayout(flmsLayout)

        return flmsGroup
    
    def plcaBox(self):
        plcaGroup = QGroupBox('PLCA')
        plcaLayout = QVBoxLayout()

        plcaLayout.addWidget(QPushButton('test'))
        plcaGroup.setLayout(plcaLayout)

        return plcaGroup

    def runBox(self):
        runGroup = QGroupBox('Supressão')
        runLayout = QHBoxLayout()

        runLayout.addWidget(QPushButton('Começar'))
        runLayout.addWidget(QPushButton('Salvar'))
        runGroup.setLayout(runLayout)

        return runGroup
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    suppressor = Suppressor()
    sys.exit(app.exec_())
