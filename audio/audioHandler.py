import soundfile as sf

def getData (audioPath):
    data = sf.read(audioPath)

    return data

def saveAs(audioArray, sampleRate, fileName='test.wav'):
    sf.write(fileName, audioArray, sampleRate, format='wav')

    print('Saved as: {}'.format(fileName))
