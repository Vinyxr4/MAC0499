from PyQt5.QtWidgets import *

def spectralSubtractionBox(mainWindow):
    specSubGroup = QGroupBox('Spectral Subtraction')
    specSubLayout = QVBoxLayout()
    specSubLayout.addStretch(1)

    estimateCheckBox = QCheckBox('Estimativa de ruído')

    specSubLayout.addWidget(estimateCheckBox)

    specSubLayout.addWidget(QLabel('Duração da estimativa (millis):'))
    estimateValue = QLineEdit()
    estimateValue.setValidator(mainWindow.onlyInt)
    estimateValue.setEnabled(True)

    estimateValue.textChanged.connect(lambda: setEstimateDuration(mainWindow, estimateValue))

    specSubLayout.addWidget(estimateValue)
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

    button = QPushButton('Selecionar áudio')
    button.clicked.connect(lambda:setAudioPath(mainWindow))
    
    runLayout.addWidget(button)
    runLayout.addWidget(QPushButton('Começar'))
    runLayout.addWidget(QPushButton('Salvar'))
    runGroup.setLayout(runLayout)

    return runGroup

def setAudioPath(mainWindow):
    mainWindow.audioPath = QFileDialog.getOpenFileName(mainWindow)
    mainWindow.statusBar().showMessage('{}'.format(mainWindow.audioPath[0]))

def setEstimateDuration(mainWindow, estimate):
    if estimate.text() != '':
        mainWindow.millisToEstimate = int(estimate.text())
        mainWindow.statusBar().showMessage('{} milisegundos'.format(mainWindow.millisToEstimate))
    else:
        mainWindow.statusBar().showMessage('')
