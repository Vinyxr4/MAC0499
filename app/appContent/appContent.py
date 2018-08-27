from PyQt5.QtWidgets import *
from app.supression.spectralSubtraction import spectralSubtraction
from app.supression.fastLMS import fastLMS
from audio import audioHandler

def spectralSubtractionBox(mainWindow):
    specSubGroup = QGroupBox('Spectral Subtraction')
    specSubLayout = QVBoxLayout()
    specSubLayout.addStretch(1)

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

def fastLMSBox(mainWindow):
    flmsGroup = QGroupBox('Fast LMS')
    flmsLayout = QVBoxLayout()

    flmsLayout.addWidget(QLabel('Número de blocos utilizados:'))
    M = QLineEdit()
    M.setPlaceholderText('100')
    M.setValidator(mainWindow.onlyInt)
    M.textChanged.connect(lambda: setBlocks(mainWindow, M))
    flmsLayout.addWidget(M)

    flmsLayout.addWidget(QLabel('Taxa de esquecimento de 0 a 100:'))
    forgetness = QLineEdit()
    forgetness.setPlaceholderText('90')
    forgetness.setValidator(mainWindow.onlyInt)
    forgetness.textChanged.connect(lambda: setForgetness(mainWindow, forgetness))
    flmsLayout.addWidget(forgetness)

    flmsLayout.addWidget(QLabel('Tamanho do passo de 0 a 100:'))
    step = QLineEdit()
    step.setPlaceholderText('10')
    step.setValidator(mainWindow.onlyInt)
    step.textChanged.connect(lambda: setStep(mainWindow, step))
    flmsLayout.addWidget(step)

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

    estimateCheckBox = QCheckBox('Estimativa de ruído')
    estimateCheckBox.clicked.connect(lambda: setEstimate(mainWindow, estimateCheckBox, pureNoise))

    audioLayout.addWidget(estimateCheckBox)

    audioLayout.addWidget(QLabel('Duração da estimativa (millis):'))
    estimateValue = QLineEdit()
    estimateValue.setPlaceholderText('100')
    estimateValue.setValidator(mainWindow.onlyInt)
    estimateValue.textChanged.connect(lambda: setEstimateDuration(mainWindow, estimateValue))
    audioLayout.addWidget(estimateValue)

    noisy = QPushButton('Áudio com ruído')
    noisy.clicked.connect(lambda:setAudioPath(mainWindow))

    pureNoise = QPushButton('Ruído puro')
    pureNoise.clicked.connect(lambda:setNoisePath(mainWindow))

    clean = QPushButton('Áudio limpo')
    clean.clicked.connect(lambda:setCleanPath(mainWindow))
    
    audioLayout.addWidget(noisy)
    audioLayout.addWidget(pureNoise)
    audioLayout.addWidget(clean)
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

def setCleanPath(mainWindow):
    mainWindow.cleanPath = QFileDialog.getOpenFileName(mainWindow)
    mainWindow.statusBar().showMessage('{}'.format(mainWindow.cleanPath[0]))

def setEstimate(mainWindow, checkBox, pureNoise):
    if checkBox.isChecked():
        mainWindow.useEstimate = True
        pureNoise.setEnabled(False)
    else:
        mainWindow.useEstimate = False
        pureNoise.setEnabled(True)

def setEstimateDuration(mainWindow, estimate):
    if estimate.text() != '':
        if int(estimate.text()) >= 100:
            mainWindow.millisToEstimate = int(estimate.text())
            mainWindow.statusBar().showMessage('{} milisegundos'.format(mainWindow.millisToEstimate))
        else:
            mainWindow.statusBar().showMessage('São necessários pelo menos 100 milisegundos!')
    else:
        mainWindow.statusBar().showMessage('')

def setBlocks(mainWindow, M):
    if M.text() != '':
        if int(M.text()) >= 1:
            mainWindow.M = int(M.text())
            mainWindow.statusBar().showMessage('{} blocos'.format(mainWindow.M))
        else:
            mainWindow.statusBar().showMessage('É necessário pelo menos um bloco!')
    else:
        mainWindow.statusBar().showMessage('')

def setForgetness(mainWindow, forgetness):
    if forgetness.text() != '':
        if int(forgetness.text()) <= 100:
            mainWindow.forgetness = (1.0 * int(forgetness.text())) / 100
            mainWindow.statusBar().showMessage('Esquecimento: {}%'.format(int(forgetness.text())))
        else:
            mainWindow.statusBar().showMessage('Não é possível passar de 100%!')
    else:
        mainWindow.statusBar().showMessage('')

def setStep(mainWindow, step):
    if step.text() != '':
        if int(step.text()) <= 100:
            mainWindow.step = (1.0 * int(step.text())) / 100
            mainWindow.statusBar().showMessage('Passo: {}%'.format(int(step.text())))
        else:
            mainWindow.statusBar().showMessage('Não é possível passar de 100!')
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
    elapsedTime = 0

    save.setEnabled(False)

    if mainWindow.algorithm[0] is True:
        noisePath = mainWindow.noisePath[0]
        useEstimate = mainWindow.useEstimate
        millis = mainWindow.millisToEstimate
        processes = mainWindow.processesAmount
        splitRate = mainWindow.splitRate
        mainWindow.suppressedAudio, mainWindow.sampleRate, elapsedTime = spectralSubtraction.spectral(audioPath, noisePath, useEstimate, millis, processes, splitRate)
    elif mainWindow.algorithm[1] is True:
        cleanPath = mainWindow.cleanPath[0]
        M = mainWindow.M
        step = mainWindow.step
        forget = mainWindow.forgetness
        mainWindow.suppressedAudio, mainWindow.sampleRate, elapsedTime = fastLMS.fastlms(audioPath, cleanPath, M, step, forget)
    # elif mainWindow.algorithm[2] is True:
    #     mainWindow.suppressedAudio, elapsedTime = spectralSubtraction.plca(audioPath, noisePath)
    
    mainWindow.statusBar().showMessage('Tempo de execução: {} segundos'.format(elapsedTime))

    save.setEnabled(True)

def saveNewAudio(mainWindow):
    fileName = 'suppressedAudio.wav'
    audioHandler.saveAs(mainWindow.suppressedAudio, mainWindow.sampleRate, fileName)
    mainWindow.statusBar().showMessage('Salvo como {}'.format('suppressedAudio.wav'))
