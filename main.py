import numpy as np
import scikits.audiolab as audiolab
import supression.spectralSubtraction as specSub
import noisy.noisy as noisy

testAudio = 'history.wav'

def audioData (audioPath):
    data = audiolab.wavread(audioPath)

    return data

def playAudio (audioArray, sampleRate):
    audiolab.play(audioArray, sampleRate)

audioArray, sampleRate, encoding = audioData(testAudio)

noisyAudio, noise = noisy.noisyArray(audioArray)

transformed = specSub.spectralSubtraction(noisyAudio)

playAudio(transformed, sampleRate)
