# import scikits.audiolab as audiolab
import soundfile as sf

def getData (audioPath):
    data = sf.read(audioPath)

    return data

# def play (audioArray, sampleRate):
#     audiolab.play(audioArray, sampleRate)

def saveAs(audioArray, sampleRate, fileName='test.wav'):
    sf.write(fileName, audioArray, sampleRate)

    print('Saved as: {}'.format(fileName))
