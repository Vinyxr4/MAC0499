import scikits.audiolab as audiolab

def getData (audioPath):
    data = audiolab.wavread(audioPath)

    return data

def play (audioArray, sampleRate):
    audiolab.play(audioArray, sampleRate)

def saveAs(audioArray, sampleRate, fileName='test.wav'):
    s = audiolab.Sndfile(fileName, mode='w', format=audiolab.Format(), channels=1, samplerate=sampleRate)
    s.write_frames(audioArray)

    print('Saved as: {}'.format(fileName))
