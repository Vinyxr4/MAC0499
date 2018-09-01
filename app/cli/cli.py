import sys
from audio import audioHandler
from app.supression.spectralSubtraction import spectralSubtraction

def throwError(error):
    errorString = ''

    if error in ['noMethod', 'invalidMethod']:
        errorString = """É necessário especificar um método válido de supressão! As opções são:\n
                      <specSub>: Subtração espectral
                      <flms>: Fast LMS
                      <plca>: Probabilistic latent component analysis\n"""

    if error in ['noNoisyPath', 'invalidNoisyPath']:
        errorString = 'É necessário especificar o arquivo de áudio a filtrar!'

    if error in ['noNoisePath', 'invalidNoisePath']:
        errorString = 'É necessário especificar o ruído a ser filtrado!'

    if error in ['notEnoughProcesses']:
        errorString = 'É necessário definir pelo menos 1 processo para esse método!'

    if error in ['notAnInt']:
        errorString = 'Esse valor precisa ser inteiro!'

    if error in ['notEnoughDurationEstimation']:
        errorString = 'É necessário especificar pelo menos 100 milissegundos para a estimativa!'

    if error in ['notEnoughSplitRate']:
        errorString = 'É necessário especificar pelo menos um bloco para esse método!'

    if error in ['invalidSavePath']:
        errorString = 'É ncessário especificar o nome utilizado para salvar o áudio suprimido!'
    
    raise ValueError(errorString)

def argumentsParser(args):
    METHOD = '--mtd'
    NOISYPATH = '--audioPath'
    SAVE = '--save'
    METHODS = ['specSub', 'flms', 'plca']
    
    if METHOD not in args:
        throwError('noMethod')
    if NOISYPATH not in args:
        throwError('noNoisyPath')

    mtdIndex = args.index(METHOD) + 1
    if mtdIndex == len(args):
        throwError('invalidMethod')

    mtdUsed = ''
    if args[mtdIndex] in METHODS:
        mtdUsed = args[mtdIndex]
    else:
        throwError('invalidMethod')

    noisyPathIndex = args.index(NOISYPATH) + 1
    if noisyPathIndex == len(args):
        throwError('noNoisyPath')

    if args[noisyPathIndex].startswith('--'):
        throwError('invalidNoisyPath')
    noisyAudioUsed = args[noisyPathIndex]

    options = {}

    if mtdUsed == METHODS[0]:
        ESTIMATE = '--estimate'
        NOESTIMATE = '--noisePath'
        SPLITRATE = '--blocks'
        PROCESSES = '--numProc'

        options['numProcesses'] = 1
        options['splitRate'] = 1
        options['estimate'] = False
        options['save'] = 'suppressed.wav'
        options['estimateDuration'] = 100
        options['noisePath'] = ''

        if SAVE in args:
            try:
                savePathIndex = args.index(SAVE) + 1
            except:
                throwError('invalidSavePath')

            try:
                if args[savePathIndex].startswith('--'):
                    throwError('invalidSavePath')
            except:
                throwError('invalidSavePath')

            options['save'] = args[savePathIndex]

        if ESTIMATE in args:
            estimateDurationIndex = args.index(ESTIMATE) + 1
            if estimateDurationIndex == len(args):
                throwError('notEnoughDurationEstimation')
            try:
                estimateDuration = int(args[estimateDurationIndex])
            except:
                throwError('notAnInt')
            if estimateDuration < 100:
                throwError('notEnoughDurationEstimation')

            options['estimateDuration'] = estimateDuration
            options['estimate'] = True
        else:
            if NOESTIMATE not in args:
                throwError('noNoisePath')

            noisePathIndex = args.index(NOESTIMATE) + 1
            if noisePathIndex == len(args):
                throwError('noNoisePath')
            if args[noisePathIndex].startswith('--'):
                throwError('invalidNoisePath')
            options['noisePath'] = args[noisePathIndex]

        if PROCESSES in args:
            numProcessesIndex = args.index(PROCESSES) + 1
            if numProcessesIndex == len(args):
                throwError('notEnoughDurationEstimation')
            try:
                numProcesses = int(args[numProcessesIndex])
            except:
                throwError('notAnInt')
            if numProcesses < 1:
                throwError('notEnoughProcesses')

            options['numProcesses'] = numProcesses

        if SPLITRATE in args:
            splitRateIndex = args.index(SPLITRATE) + 1
            if splitRateIndex == len(args):
                throwError('notEnoughSplitRate')
            try:
                splitRate = int(args[splitRateIndex])
            except:
                throwError('notAnInt')
            
            if splitRate < 1:
                throwError('notEnoughSplitRate')

            options['splitRate'] = args[splitRateIndex]

    elif mtdUsed == METHODS[1]:
        options['M'] = 100
        options['step'] = 0.1
        options['forgetness'] = 0.9

    return mtdUsed, noisyAudioUsed, options
        
if __name__ == '__main__':
    
    methodUsed, audioPath, options = argumentsParser(sys.argv[1:])

    print(methodUsed, audioPath, options)

    if methodUsed == 'specSub':
        audioPath = audioPath

        noisePath = options['noisePath']
        milliSeconds = int(options['estimateDuration'])
        useEstimate = bool(options['estimate'])
        processes = int(options['numProcesses'])
        splitRate = int(options['splitRate'])

        suppressed, sampleRate, elapsed = spectralSubtraction.spectral(audioPath, noisePath, useEstimate, milliSeconds, processes, splitRate)

        print('Tempo de execução: {} segundos'.format(elapsed))
        audioHandler.saveAs(suppressed, sampleRate, options['save'])
