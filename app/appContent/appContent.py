from PyQt5.QtWidgets import *
from app.supression.spectralSubtraction import spectralSubtraction
from audio import audioHandler

def spectralSubtractionBox(mainWindow):
    specSubGroup = QGroupBox('Spectral Subtraction')
    specSubLayout = QVBoxLayout()
    specSubLayout.addStretch(1)

    estimateCheckBox = QCheckBox('Estimativa de ruído')
    estimateCheckBox.clicked.connect(lambda: setEstimate(mainWindow, estimateCheckBox))

    specSubLayout.addWidget(estimateCheckBox)

    specSubLayout.addWidget(QLabel('Duração da estimativa (millis):'))
    estimateValue = QLineEdit()
    estimateValue.setPlaceholderText('100')
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
    spectralOption.clicked.connect(lambda:setAlgorithm(mainWindow, 0))
    flmsOption = QRadioButton('Fast LMS')
    flmsOption.clicked.connect(lambda:setAlgorithm(mainWindow, 1))
    plcaOption = QRadioButton('PLCA')
    plcaOption.clicked.connect(lambda:setAlgorithm(mainWindow, 2))

    selectLayout.addWidget(spectralOption)
    selectLayout.addWidget(flmsOption)
    selectLayout.addWidget(plcaOption)
    selectGroup.setLayout(selectLayout)

    return selectGroup

def runBox(mainWindow):
    runGroup = QGroupBox('Supressão')
    runLayout = QVBoxLayout()

    start = QPushButton('Começar')
    save = QPushButton('Salvar')
    save.setEnabled(False)

    runLayout.addWidget(start)
    start.clicked.connect(lambda:runSuppression(mainWindow, save))

    runLayout.addWidget(save)
    save.clicked.connect(lambda:saveNewAudio(mainWindow))

    runGroup.setLayout(runLayout)

    return runGroup

def setAudioPath(mainWindow):
    mainWindow.audioPath = QFileDialog.getOpenFileName(mainWindow)
    mainWindow.statusBar().showMessage('{}'.format(mainWindow.audioPath[0]))

def setNoisePath(mainWindow):
    mainWindow.noisePath = QFileDialog.getOpenFileName(mainWindow)
    mainWindow.statusBar().showMessage('{}'.format(mainWindow.noisePath[0]))

def setEstimate(mainWindow, checkBox):
    if checkBox.isChecked():
        mainWindow.useEstimate = True
    else:
        mainWindow.useEstimate = False

def setEstimateDuration(mainWindow, estimate):
    if estimate.text() != '':
        if int(estimate.text()) >= 100:
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

def setAlgorithm(mainWindow, index):
    if mainWindow.algorithm[index] is False:
        mainWindow.algorithm[0] = False
        mainWindow.algorithm[1] = False
        mainWindow.algorithm[2] = False
        mainWindow.algorithm[index] = True

def runSuppression(mainWindow, save):
    audioPath = mainWindow.audioPath[0]
    noisePath = mainWindow.noisePath[0]
    useEstimate = mainWindow.useEstimate

    elapsedTime = 0

    save.setEnabled(False)

    if mainWindow.algorithm[0] is True:
        mainWindow.suppressedAudio, mainWindow.sampleRate, elapsedTime = spectralSubtraction.spectral(audioPath, noisePath, useEstimate=useEstimate)
    # elif mainWindow.algorithm[1] is True:
    #     mainWindow.suppressedAudio, elapsedTime = spectralSubtraction.flms(audioPath, noisePath)
    # elif mainWindow.algorithm[2] is True:
    #     mainWindow.suppressedAudio, elapsedTime = spectralSubtraction.plca(audioPath, noisePath)
    
    mainWindow.statusBar().showMessage('Tempo de execução: {} segundos'.format(elapsedTime))

    save.setEnabled(True)

def saveNewAudio(mainWindow):
    fileName = 'suppressedAudio.wav'
    audioHandler.saveAs(mainWindow.suppressedAudio, mainWindow.sampleRate, fileName)
    mainWindow.statusBar().showMessage('Salvo como {}'.format('suppressedAudio.wav'))
