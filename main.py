import numpy as np
import scikits.audiolab as audiolab

testAudio = 'history.wav'

def audioData (audioPath):
    data = audiolab.wavread(audioPath)

    return data

def playAudio (audioArray, sampleRate):
    audiolab.play(audioArray, sampleRate)

data = audioData(testAudio)
print(data[0])

playAudio(data[0], data[1])
