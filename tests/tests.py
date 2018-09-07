import audio.audioHandler as audio
import numpy as np
import matplotlib.pyplot as plt
import csv
import time

from app.supression.spectralSubtraction import spectralSubtraction
from app.supression.fastLMS import fastLMS
from app.supression.plca import plcaWavelet

def runTests():
    audioPrefix = 'audio_files/'

    resultPrefix = 'results/'
    # audioLengthMultipliers = [2, 4, 10]
    audioLengthMultipliers = [10]
    repetitions = 20
    
    audioFile = 'die_hard'
    # noiseFiles = ['echoPlanar', 'diffusion', 'fastSpinEcho']
    noiseFiles = ['echoPlanar', 'diffusion', 'fastSpinEcho']
        
    methods = ['spectralSubtraction', 'flms', 'plcaWavelet']
    # methods = ['plcaWavelet']

    audioArray, sampleRate = audio.getData(audioPrefix + audioFile + '.wav')
    audioArray = audioArray[:sampleRate * 30]

    headers = ['']
    content = []

    testsAmount = repetitions * len(noiseFiles) * len(audioLengthMultipliers) * len(methods)

    start = time.time()

    current = 0
    for multiplier in audioLengthMultipliers:
        testAudio = np.tile(audioArray, multiplier)

        cleanFile = resultPrefix + 'cleanAudios/clean_' + audioFile + str(30 * multiplier) + '.wav'
        audio.saveAs(testAudio, sampleRate, cleanFile)
        n = 1
        for noiseFile in noiseFiles:
            noise, sampleRate = audio.getData(audioPrefix + noiseFile + '.wav')
            noise = [row[0] for row in noise[:sampleRate * 5]]

            testNoise = np.tile(noise, multiplier * 6)

        
            testNoise = testNoise * 4

            noiseTransf = np.fft.fft(testNoise)
            audioTransf = np.fft.fft(testAudio)
            noisy = np.fft.ifft(noiseTransf + audioTransf).real
            
            noisyFile = resultPrefix + 'noisyAudios/noisy' + noiseFile + str(30 * multiplier) + '.wav'
            audio.saveAs(noisy, sampleRate, noisyFile)

            testNoiseFile = resultPrefix + 'noiseAudios/test' + noiseFile + str(30 * multiplier) + '.wav'
            audio.saveAs(testNoise, sampleRate, testNoiseFile)

            n += 1

            mix = plt.figure(1)
            sep = plt.figure(2)
            ax = mix.add_subplot(111)
            bx = sep.add_subplot(111)

            for method in methods:
                print('Running for {} on noise {} with length {}'.format(method, noiseFile, 30 * multiplier))

                headers.append('{}_{}_{}'.format(method, noiseFile, 30 * multiplier))

                times = np.zeros(repetitions)

                for turn in range(repetitions):
                    if method == 'spectralSubtraction':
                        suppressedAudio, sampleRate, elapsed = spectralSubtraction.spectral(noisyFile, testNoiseFile, useEstimate=False, splitRate=4)
                    elif method == 'flms':
                        suppressedAudio, sampleRate, elapsed = fastLMS.fastlms(noisyFile, cleanFile)
                    else:
                        blks = int((multiplier * 30) / 60) + 1
                        suppressedAudio, sampleRate, elapsed = plcaWavelet.plca(noisyFile, testNoiseFile, 10)
                    
                    current += 1
                    currentPerc = round((100.0 * current) / testsAmount, 3)

                    now = time.time() - start

                    remain = round((100.0 - currentPerc) * (now / currentPerc), 2)

                    print('********** {}% completo, {} segundos restantes **********'.format(currentPerc, remain))

                    times[turn] = elapsed

                content.append(round(np.mean(times), 6))
                content.append(round(np.std(times), 6))
                content.append(round(np.var(times), 6))
                content.append(round(((suppressedAudio - testAudio) ** 2).mean(), 6))

                bx.magnitude_spectrum(suppressedAudio, Fs=sampleRate)
                ax.magnitude_spectrum(suppressedAudio, Fs=sampleRate)
                sep.savefig(resultPrefix + 'suppressedSpectra/suppressed' + method + noiseFile + str(30 * multiplier) + '.png')
                bx.clear()

                suppressedFile = resultPrefix + 'suppressedAudios/suppressed' + method + noiseFile + str(30 * multiplier) + '.wav'
                audio.saveAs(suppressedAudio, sampleRate, suppressedFile)
            
            mix.savefig(resultPrefix + 'suppressedSpectra/suppressed' + noiseFile + str(30 * multiplier) + '.png')
    
    with open('{}results_{}.csv'.format(resultPrefix, 10 * 30), 'w') as csvfile:
        fileWritter = csv.writer(csvfile, delimiter=',')

        fileWritter.writerow(headers)
        
        mean = []
        std = []
        var = []
        error = []

        for i in range(0, len(content), 4):
            mean.append(content[i])
            std.append(content[i+1])
            var.append(content[i+2])
            error.append(content[i+3])

        fileWritter.writerow(['Mean time'] + mean)
        fileWritter.writerow(['Time stdDev'] + std)
        fileWritter.writerow(['Time var'] + var)
        fileWritter.writerow(['Squared Error'] + error)

runTests()