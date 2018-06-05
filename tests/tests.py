import audio.audioHandler as audio
import supression.spectralSubtraction as specSub
import noisy.noisy as noisy

def spectral(audioPath, freq=500, useEstimate=False, noiseType='sin', amplitude = 0.2, seconds = 0.01):
    testAudio = audioPath

    audioArray, sampleRate, encoding = audio.getData(testAudio)

    noisyAudio = None
    noise = None
    if noiseType == 'sin':
        noisyAudio, noise = noisy.sinNoise(audioArray, sampleRate, freq, amplitude)
    elif noiseType == 'random':
        noisyAudio, noise = noisy.randomNoise(audioArray, amplitude)

    if useEstimate is True:
        noise = None

    firstPeriod = seconds * sampleRate

    suppressedAudio, noiseUsed = specSub.spectralSubtraction(noisyAudio, noiseArray=noise, estimate=firstPeriod)

    return suppressedAudio, noisyAudio, sampleRate, noiseUsed
