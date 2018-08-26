from supression import spectralSubtraction as specSub
from audio import audioHandler

def spectral(audioPath, noisePath, useEstimate=True, milliSeconds = 100, processes=4, splitRate=1):
    audioArray, noiseArray, sampleRate = prepare(audioPath, noisePath, useEstimate)

    firstPeriod = ((1.0 * milliSeconds) / 1000) * sampleRate
    
    suppressedAudio, noiseUsed, elapsedTime = specSub.spectralSubtraction(audioArray, noiseArray=noiseArray, estimate=firstPeriod, processes=processes, splitRate=splitRate)
    return suppressedAudio, elapsedTime

def prepare(audioPath, noisePath, useEstimate):
    audioArray, sampleRate = audioHandler.getData(audioPath)
    
    noiseArray = None
    if useEstimate is False:
        noiseArray, noiseSampleRate = audio.getData(noisePath)
        
    return audioArray, noiseArray, sampleRate
