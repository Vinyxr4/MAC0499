from supression import Plca
from audio import audioHandler

def plca(audioPath, noisePath, iterations):
    noiseArray, noisyArray, sampleRate = prepare(audioPath, noisePath)

    suppressedAudio, noise, elapsedTime = Plca.plca(noisyArray, noiseArray, iterations)

    return suppressedAudio, sampleRate, elapsedTime


def prepare(audioPath, noisePath):
    noisyArray, sampleRate = audioHandler.getData(audioPath)
    
    noiseArray, noiseSampleRate = audioHandler.getData(noisePath)
        
    return noiseArray, noisyArray, sampleRate
