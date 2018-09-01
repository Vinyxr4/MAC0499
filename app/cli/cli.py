import sys

def throwError(error):
    errorString = ''

    if error in ['noMethod', 'invalidMethod']:
        errorString = """É necessário especificar um método válido de supressão! As opções são:\n
                      <specSub>: Subtração espectral
                      <flms>: Fast LMS
                      <plca>: Probabilistic latent component analysis\n"""

    if error in ['noNoisyPath', 'invalidNoisyPath']:
        errorString = 'É necessário especificar o arquivo de áudio a filtrar!'
    
    raise ValueError(errorString)

def argumentsParser(args):
    METHOD = '--mtd'
    NOISYPATH = '--npath'
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
        options['numProcesses'] = 1
        options['splitRate'] = 1
        options['estimate'] = True
        options['estimateDuration'] = 100
    elif mtdUsed == METHODS[1]:
        options['M'] = 100
        options['step'] = 0.1
        options['forgetness'] = 0.9

    return mtdUsed, noisyAudioUsed, options
        
if __name__ == '__main__':
    
    print(argumentsParser(sys.argv[1:]))
