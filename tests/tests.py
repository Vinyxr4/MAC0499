import audio.audioHandler as audio
import supression.spectralSubtraction as specSub
import supression.fastLMS as flms
import noisy.noisy as noisy

def spectral(audioPath, freq=500, useEstimate=False, noiseType='sin', amplitude = 0.2, seconds = 0.01, processes=4, splitRate=1, method='spectral'):
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

    noiseUsed = noise
    suppressedAudio = []
    elapsedTime = 0
    if method == 'spectral':
        suppressedAudio, noiseUsed, elapsedTime = specSub.spectralSubtraction(noisyAudio, noiseArray=noise, estimate=firstPeriod, processes=processes, splitRate=splitRate)
    elif method == 'flms':
        suppressedAudio, elapsedTime = flms.fastLms(noisyAudio, audioArray, 100, step=0.5, forgetness=0.7)


    return suppressedAudio, noisyAudio, sampleRate, noiseUsed, elapsedTime
