import numpy as np

def spectralSubtraction (audioArray, noiseArray = None, estimate = 0.01):
    if noiseArray is None:
        lastOnRange = int(np.floor(estimate))
        print(lastOnRange)
        noiseEstimate = audioArray[0:lastOnRange]

        repetitions = int(np.floor(audioArray.size/noiseEstimate.size))

        noiseArray = np.tile(noiseEstimate, repetitions)
        noiseArray = np.append(noiseArray, noiseEstimate[0:audioArray.size - noiseArray.size])
    elif noiseArray.size < audioArray.size:
        repetitions = int(np.floor(audioArray.size/noiseArray.size))

        noiseArray = np.tile(noiseArray, repetitions)
        noiseArray = np.append(noiseArray, noiseArray[0:audioArray.size - noiseArray.size])
    elif noiseArray.size > audioArray.size:
        noiseArray = noiseArray[0:audioArray.size]

    transformedAudio = np.fft.fft(audioArray)
    tranfAudiophase = np.angle(transformedAudio)
    tranfAudioAmp = np.absolute(transformedAudio)
    audioPwr = tranfAudioAmp ** 2

    transformedNoise = np.fft.fft(noiseArray)
    tranfNoiseAmp = np.absolute(transformedNoise)
    noisePwr = tranfNoiseAmp ** 2

    subtraction = audioPwr - noisePwr
    subtraction = np.maximum(subtraction, 0)
    subtraction = np.sqrt(subtraction)

    suppressedFreqDomain = subtraction * np.exp(tranfAudiophase * 1j)

    suppressedAudio = np.fft.ifft(suppressedFreqDomain).real

    return suppressedAudio, noiseArray
