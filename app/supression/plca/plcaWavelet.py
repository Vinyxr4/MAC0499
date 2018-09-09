from supression import Plca
from audio import audioHandler
import time
import numpy as np

def allPlca(audioPath, noisePath, iterations, splitRate):
    noiseArray, audioArray, sampleRate = prepare(audioPath, noisePath)
    
    elapsed = time.time()
    
    lastBlockSize = len(audioArray) % splitRate

    blkSize = int((len(audioArray) - lastBlockSize) / splitRate)
    
  #  print(blkSize)
    lastBlockAudio = audioArray[len(audioArray) - lastBlockSize - blkSize:]
    lastBlockNoise = audioArray[len(noiseArray) - lastBlockSize - blkSize:]

    result = np.zeros(1)

    for i in range(splitRate - 1):
        currentAudio = audioArray[i * blkSize: (i+1)*blkSize]
        currentNoise = noiseArray[i * blkSize: (i+1)*blkSize]

#        print(len(currentAudio))

        currentArray, currentNoise, dummy = Plca.plca(currentAudio, currentNoise, 10)

        offset = 0
        if lastBlockSize > 0:
 #           print('pudim')
            offset = 1

        result = np.append(result, currentArray[offset:])

    lasArray, lastNoise, dummy = Plca.plca(lastBlockAudio, lastBlockNoise, 10)
    result = np.append(result, lasArray)

    return result[1:], sampleRate, time.time() - elapsed

def plca(audioPath, noisePath, iterations):
    noiseArray, noisyArray, sampleRate = prepare(audioPath, noisePath)

    suppressedAudio, noise, elapsedTime = Plca.plca(noisyArray, noiseArray, iterations)

    return suppressedAudio, sampleRate, elapsedTime

def prepare(audioPath, noisePath):
    noisyArray, sampleRate = audioHandler.getData(audioPath)
    
    noiseArray, noiseSampleRate = audioHandler.getData(noisePath)
        
    return noiseArray, noisyArray, sampleRate
