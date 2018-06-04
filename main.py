import audio.audioHandler as audio
import supression.spectralSubtraction as specSub
import noisy.noisy as noisy
import tests.tests as test

testAudio = 'history.wav'

suppressedAudio, noisyAudio, sampleRate = test.spectral(testAudio, useEstimate=True)

audio.play(noisyAudio, sampleRate)
audio.play(suppressedAudio, sampleRate)
