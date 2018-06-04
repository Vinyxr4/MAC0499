import scikits.audiolab as audiolab

def getData (audioPath):
    data = audiolab.wavread(audioPath)

    return data

def play (audioArray, sampleRate):
    audiolab.play(audioArray, sampleRate)
