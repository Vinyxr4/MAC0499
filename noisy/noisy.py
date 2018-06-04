import numpy as np

def noisyArray (array, noiseRate = 0.5, amplitude = 0.2):
    noise = amplitude * np.random.random_sample((array.size,)) - (amplitude * (1 - noiseRate))

    noisyArray = array + noise

    return noisyArray, noise
