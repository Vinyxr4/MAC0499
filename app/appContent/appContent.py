from PyQt5.QtWidgets import *

def spectralSubtractionBox():
    specSubGroup = QGroupBox('Spectral Subtraction')
    specSubLayout = QVBoxLayout()

    specSubLayout.addWidget(QPushButton('test'))
    specSubGroup.setLayout(specSubLayout)

    return specSubGroup

def fastLMSBox():
    flmsGroup = QGroupBox('Fast LMS')
    flmsLayout = QVBoxLayout()

    flmsLayout.addWidget(QPushButton('test'))
    flmsGroup.setLayout(flmsLayout)

    return flmsGroup

def plcaBox():
    plcaGroup = QGroupBox('PLCA')
    plcaLayout = QVBoxLayout()

    plcaLayout.addWidget(QPushButton('test'))
    plcaGroup.setLayout(plcaLayout)

    return plcaGroup

def runBox(mainWindow):
    runGroup = QGroupBox('Supressão')
    runLayout = QHBoxLayout()

    button = QPushButton('Set audio')
    button.clicked.connect(lambda:setAudioPath(mainWindow))
    
    runLayout.addWidget(button)
    runLayout.addWidget(QPushButton('Começar'))
    runLayout.addWidget(QPushButton('Salvar'))
    runGroup.setLayout(runLayout)

    return runGroup

def setAudioPath(mainWindow):
    mainWindow.audioPath = QFileDialog.getOpenFileName(mainWindow)
    mainWindow.statusBar().showMessage('{}'.format(mainWindow.audioPath[0]))
