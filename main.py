import numpy as np
import pyaudio
import wave
from scipy.io import wavfile

def audioData (audioPath):
    data = wavfile.read(audioPath)

    return data
