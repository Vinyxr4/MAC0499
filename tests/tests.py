import audio.audioHandler as audio
import supression.spectralSubtraction as specSub
import supression.fastLMS as flms
import noisy.noisy as noisy
import numpy as np
import matplotlib.pyplot as plt
import math

def prepare(audioPath, useEstimate, noiseType, freq, amplitude):
    audioArray, sampleRate = audio.getData(audioPath)

    noisyAudio = None
    noise = None

    if noiseType == 'sin':
        noisyAudio, noise = noisy.sinNoise(audioArray, sampleRate, freq, amplitude)
    elif noiseType == 'random':
        noisyAudio, noise = noisy.randomNoise(audioArray, amplitude)

    if useEstimate:
        noise = None

    return audioArray, sampleRate, noisyAudio, noise

def fitArray(arr1, arr2):
    fittedArr = arr1

    if arr1.size < arr2.size:
        repetitions = int(np.floor(arr2.size/arr1.size))
        fittedArr = np.tile(fittedArr, repetitions)
        fittedArr = np.append(fittedArr, fittedArr[0:arr2.size - fittedArr.size])
    elif arr1.size > arr2.size:
        fittedArr = arr1[0:arr2.size]

    return fittedArr

def fastlms(audioPath, freq=1000, noiseType='sin', amplitude=0.1, M=1000, step=0.1, forget=0.9):
    audioArray, sampleRate, noisyAudio, noise = prepare(audioPath, False, noiseType, freq, amplitude)    
    
    t = int(math.floor(1.2*sampleRate/freq))

    noiseArray = None
    if noiseArray is None:
        lastOnRange = int(np.floor(sampleRate/freq))
        noiseEstimate = noisyAudio[0:lastOnRange]

        repetitions = int(np.floor(noisyAudio.size/noiseEstimate.size))

        noiseArray = np.tile(noiseEstimate, repetitions)
        noiseArray = np.append(noiseArray, noiseEstimate[0:noisyAudio.size - noiseArray.size])
    
    desiredArray = np.append(np.zeros(t), noisyAudio[:-t])

    suppressedAudio, elapsedTime = flms.fastLms(noisyAudio, desiredArray, M, step=step, forgetness=forget)

    # print(np.mean((audioArray-suppressedAudio)**2))

    return suppressedAudio, noisyAudio, sampleRate, noise, elapsedTime

def plotResult(audioArray, noisyAudio, suppressedAudio, save=False):
    time_step = 1.0 / 30
    freqs = np.fft.fftfreq(audioArray.size, time_step)
    idx = np.argsort(freqs)

    original = np.absolute(np.fft.fft(audioArray))**2
    noisy = np.absolute(np.fft.fft(noisyAudio))**2
    suppressed = np.absolute(np.fft.fft(suppressedAudio))**2
    plt.plot(freqs[idx], original[idx])
    if save:
        plt.savefig('originalPwr.png')
    plt.show()

    plt.plot(freqs[idx], noisy[idx])
    if save:
        plt.savefig('noisyPwr.png')
    plt.show()

    plt.plot(freqs[idx], suppressed[idx])
    if save:
        plt.savefig('suppressedPwr.png')
    plt.show()

def spectral(audioPath, freq=1000, useEstimate=True, noiseType='sin', amplitude = 0.1, seconds = 0.01, processes=4, splitRate=1):
    audioArray, sampleRate, noisyAudio, noise = prepare(audioPath, useEstimate, noiseType, freq, amplitude)    

    firstPeriod = seconds * sampleRate
    
    suppressedAudio, noiseUsed, elapsedTime = specSub.spectralSubtraction(noisyAudio, noiseArray=noise, estimate=firstPeriod, processes=processes, splitRate=splitRate)
    print(np.mean((audioArray-noisyAudio)**2))
    print(np.mean((audioArray-suppressedAudio)**2))
    return suppressedAudio, noisyAudio, sampleRate, noiseUsed, elapsedTime
