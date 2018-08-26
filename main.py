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

testAudio = '{}/{}.wav'.format(audio_path, audios[0])

audioArray, sampleRate = audio.getData(testAudio)

totalSeconds = 1.0 * audioArray.size / sampleRate

instances = int(totalSeconds / 2)

suppressedAudio, noisyAudio, sampleRate, noise, elapsedTime = test.spectral(testAudio)
# suppressedAudio, noisyAudio, sampleRate, noise, elapsedTime = test.fastlms(testAudio)

print(elapsedTime)

print('Noisy audio:')
# audio.play(noisyAudio, sampleRate)
audio.saveAs(noisyAudio, sampleRate, 'noisy.wav')

print('Spectral supressed audio:')
audio.saveAs(suppressedAudio, sampleRate, 'test.wav')

# plca.plca(noisyAudio, sampleRate)
