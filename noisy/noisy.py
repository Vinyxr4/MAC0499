import numpy as np

def randomNoise (array, amplitude = 0.2):
    reajustRange = 0.5
    noise = amplitude * np.random.random_sample((array.size,)) - (amplitude * reajustRange)

    noisyArray = array + noise

    return noisyArray, noise

def sinNoise (array, frequency = 1.0, amplitude = 0.2):
    samples = np.linspace(0, frequency * 2 * np.pi, array.size)

    noise = amplitude * np.sin(samples)
    noisyArray = array + noise

    return noisyArray, noise
