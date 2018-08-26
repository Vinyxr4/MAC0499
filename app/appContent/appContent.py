from PyQt5.QtWidgets import *

def spectralSubtractionBox(mainWindow):
    specSubGroup = QGroupBox('Spectral Subtraction')
    specSubLayout = QVBoxLayout()
    specSubLayout.addStretch(1)

    estimateCheckBox = QCheckBox('Estimativa de ruído')

    specSubLayout.addWidget(estimateCheckBox)

    specSubLayout.addWidget(QLabel('Duração da estimativa (millis):'))
    estimateValue = QLineEdit()
    estimateValue.setPlaceholderText('1')
    estimateValue.setValidator(mainWindow.onlyInt)
    estimateValue.textChanged.connect(lambda: setEstimateDuration(mainWindow, estimateValue))
    specSubLayout.addWidget(estimateValue)

    specSubLayout.addWidget(QLabel('Número de processos utilizados:'))
    processes = QLineEdit()
    processes.setPlaceholderText('1')
    processes.setValidator(mainWindow.onlyInt)
    processes.textChanged.connect(lambda: setProcessesAmount(mainWindow, processes))
    specSubLayout.addWidget(processes)

    specSubLayout.addWidget(QLabel('Número de blocos utilizados:'))
    splitRate = QLineEdit()
    splitRate.setPlaceholderText('1')
    splitRate.setValidator(mainWindow.onlyInt)
    splitRate.textChanged.connect(lambda: setSplitRate(mainWindow, splitRate))
    specSubLayout.addWidget(splitRate)

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

def audioBox(mainWindow):
    audioGroup = QGroupBox('Selecionar')
    audioLayout = QVBoxLayout()

    noisy = QPushButton('Áudio com ruído')
    noisy.clicked.connect(lambda:setAudioPath(mainWindow))

    pureNoise = QPushButton('Ruído puro')
    pureNoise.clicked.connect(lambda:setNoisePath(mainWindow))
    
    audioLayout.addWidget(noisy)
    audioLayout.addWidget(pureNoise)
    audioGroup.setLayout(audioLayout)

    return audioGroup

def selectBox(mainWindow):
    selectGroup = QGroupBox('Método Utilizado')
    selectLayout = QVBoxLayout()

    spectralOption = QRadioButton('Subtração spectral')
    flmsOption = QRadioButton('Fast LMS')
    plcaOption = QRadioButton('PLCA')

    spectralOption.click()

    selectLayout.addWidget(spectralOption)
    selectLayout.addWidget(flmsOption)
    selectLayout.addWidget(plcaOption)
    selectGroup.setLayout(selectLayout)

    return selectGroup

def runBox(mainWindow):
    runGroup = QGroupBox('Supressão')
    runLayout = QVBoxLayout()

    runLayout.addWidget(QPushButton('Começar'))
    runLayout.addWidget(QPushButton('Salvar'))
    runGroup.setLayout(runLayout)

    return runGroup

def setAudioPath(mainWindow):
    mainWindow.audioPath = QFileDialog.getOpenFileName(mainWindow)
    mainWindow.statusBar().showMessage('{}'.format(mainWindow.audioPath[0]))

def setNoisePath(mainWindow):
    mainWindow.noisePath = QFileDialog.getOpenFileName(mainWindow)
    mainWindow.statusBar().showMessage('{}'.format(mainWindow.noisePath[0]))

def setEstimateDuration(mainWindow, estimate):
    if estimate.text() != '':
        if int(estimate.text()) > 100:
            mainWindow.millisToEstimate = int(estimate.text())
            mainWindow.statusBar().showMessage('{} milisegundos'.format(mainWindow.millisToEstimate))
        else:
            mainWindow.statusBar().showMessage('São necessários pelo menos 100 milisegundos!')
    else:
        mainWindow.statusBar().showMessage('')

def setProcessesAmount(mainWindow, processes):
    if processes.text() != '':
        if int(processes.text()) > 0:
            mainWindow.processesAmount = int(processes.text())
            mainWindow.statusBar().showMessage('{} processos executarão a supressão'.format(mainWindow.processesAmount))
        else:
            mainWindow.statusBar().showMessage('É necessário utilizar pelo menos um processo!')

    else:
        mainWindow.statusBar().showMessage('')

def setSplitRate(mainWindow, splitRate):
    if splitRate.text() != '':
        if int(splitRate.text()) > 0:
            mainWindow.splitRate = int(splitRate.text())
            mainWindow.statusBar().showMessage('{} blocos para realizar a supressão'.format(mainWindow.splitRate))
        else:
            mainWindow.statusBar().showMessage('É necessário utilizar pelo menos um bloco!')

    else:
        mainWindow.statusBar().showMessage('')
