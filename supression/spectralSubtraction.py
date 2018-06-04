import numpy as np

def spectralSubtraction (audioArray, noiseArray = None, estimate = 0.01):
    if noiseArray is None:
        lastOnRange = int(np.floor(audioArray.size * estimate))
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
    transformedNoise = np.fft.fft(noiseArray)
    subtraction = transformedAudio - transformedNoise

    supressedAudio = np.fft.ifft(subtraction).real

    return supressedAudio
