import audio.audioHandler as audio
import supression.spectralSubtraction as specSub
import noisy.noisy as noisy
import tests.tests as test
import numpy as np

testAudio = 'history.wav'

suppressedAudio, noisyAudio, sampleRate, noise = test.spectral(testAudio, useEstimate=True)

print('Noisy audio:')
audio.play(noisyAudio, sampleRate)

print('Spectral supressed audio:')
audio.play(suppressedAudio, sampleRate)

audioArray, sampleRate, encoding = audio.getData(testAudio)

audio.play(noise, sampleRate)

print('Signal domain suppresed audio:')
audio.play(noisyAudio - noise, sampleRate)
