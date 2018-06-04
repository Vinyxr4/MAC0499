import audio.audioHandler as audio
import supression.spectralSubtraction as specSub
import noisy.noisy as noisy

def spectral(audioPath, freq=3000, useEstimate=False, noiseType='sin', amplitude = 0.1):
    testAudio = audioPath

    audioArray, sampleRate, encoding = audio.getData(testAudio)

    noisyAudio = None
    noise = None
    if noiseType == 'sin':
        noisyAudio, noise = noisy.sinNoise(audioArray, freq, amplitude)
    elif noiseType == 'random':
        noisyAudio, noise = noisy.randomNoise(audioArray, amplitude)

    if useEstimate is True:
        noise = None

    firstPeriod = 1.0 * freq / audioArray.size

    suppressedAudio = specSub.spectralSubtraction(noisyAudio, noiseArray=noise, estimate=firstPeriod)

    return suppressedAudio, noisyAudio, sampleRate
