import audio.audioHandler as audio
import supression.spectralSubtraction as specSub
import supression.fastLMS as flms
import noisy.noisy as noisy
import tests.tests as test
import numpy as np
import multiprocessing as mp

import supression.Plca as plca

audio_path = 'audio_files'
audios = ['history', 'die_hard']

testAudio = '{}/{}.wav'.format(audio_path, audios[1])

audioArray, sampleRate = audio.getData(testAudio)
audioArray = audioArray[:22000]

totalSeconds = 1.0 * audioArray.size / sampleRate

instances = int(totalSeconds / 2)

suppressedAudio, noisyAudio, sampleRate, noise, elapsedTime = test.spectral(testAudio)
# suppressedAudio, noisyAudio, sampleRate, noise, elapsedTime = test.fastlms(testAudio)

audio.saveAs(noise, sampleRate, 'pureNoise2.wav')

# print(elapsedTime)

# print('Noisy audio:')
# # audio.play(noisyAudio, sampleRate)
audio.saveAs(noisyAudio, sampleRate, 'noisy2.wav')

# print('Spectral supressed audio:')
# audio.saveAs(suppressedAudio, sampleRate, 'test.wav')

# plca.plca(noisyAudio, sampleRate)
