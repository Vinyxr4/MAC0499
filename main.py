import audio.audioHandler as audio
import supression.spectralSubtraction as specSub
import supression.fastLMS as flms
import noisy.noisy as noisy
import tests.tests as test
import numpy as np
import multiprocessing as mp


testAudio = 'die_hard.wav'

audioArray, sampleRate, encoding = audio.getData(testAudio)

totalSeconds = 1.0 * audioArray.size / sampleRate

instances = int(totalSeconds / 2)

# suppressedAudio, noisyAudio, sampleRate, noise, elapsedTime = test.spectral(testAudio, processes=instances, seconds=0.01, splitRate=instances)
suppressedAudio, noisyAudio, sampleRate, noise, elapsedTime = test.fastlms(testAudio)

print(elapsedTime)

print('Noisy audio:')
audio.play(noisyAudio, sampleRate)

print('Spectral supressed audio:')
audio.saveAs(suppressedAudio, sampleRate, 'test.wav')
