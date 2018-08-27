from supression import fastLMS as flms
from audio import audioHandler

def fastlms(audioPath, cleanPath, M=1000, step=0.1, forget=0.9):
    cleanArray, noisyArray, sampleRate = prepare(audioPath, cleanPath)
    
    desiredArray = cleanArray

    suppressedAudio, elapsedTime = flms.fastLms(noisyArray, desiredArray, M, step=step, forgetness=forget)

    return suppressedAudio, sampleRate, elapsedTime

def prepare(audioPath, cleanPath):
    noisyArray, sampleRate = audioHandler.getData(audioPath)
    
    cleanArray, cleanSampleRate = audioHandler.getData(cleanPath)
        
    return cleanArray, noisyArray, sampleRate
