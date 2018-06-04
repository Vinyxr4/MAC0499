import numpy as np

def spectralSubtraction (audioArray):
    transformedAudio = np.fft.fft(audioArray)
    transformedAudio = np.fft.ifft(transformedAudio)

    print(transformedAudio.real)
    return transformedAudio
