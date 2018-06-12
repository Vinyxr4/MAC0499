import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp

import time

def spectralSubtraction (audioArray, noiseArray = None, estimate = 0.01, splitRate = 1, processes = 4):
    audioArrays = np.array_split(audioArray, splitRate)

    audioSizes = np.zeros(len(audioArrays) + 1, dtype=int)
    for i in range(len(audioArrays)):
        audioSizes[i+1] = audioSizes[i] + audioArrays[i].size

    if noiseArray is None:
        lastOnRange = int(np.floor(estimate))
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

    noiseArrays = [noiseArray[audioSizes[j]:audioSizes[j+1]] for j in range(len(audioArrays))]

    startTime = time.time()
    pool = mp.Pool(processes=processes)

    results = [pool.apply(spectralChunk,
                    args=(audioArrays[i], noiseArrays[i], ))
                    for i in range(len(audioArrays))
              ]

    suppressedAudio = np.concatenate(results).ravel()
    #suppressedAudio = spectralChunk(audioArray, noiseArray)
    elapsedTime = time.time() - startTime

    """time_step = 1.0 / 30
    freqs = np.fft.fftfreq(audioArray.size, time_step)
    idx = np.argsort(freqs)

    plt.plot(freqs[idx], audioPwr[idx])
    plt.savefig('test.png')
    plt.plot(freqs[idx], noisePwr[idx])
    plt.show()
    plt.plot(freqs[idx], subtraction[idx])
    plt.show()"""

    return suppressedAudio, noiseArray, elapsedTime

def spectralChunk(audioArray, noiseArray):
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

    return suppressedAudio
