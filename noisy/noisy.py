import numpy as np
import math

def randomNoise (array, amplitude = 0.2):
    reajustRange = 0.5
    noise = amplitude * np.random.random_sample((array.size,)) - (amplitude * reajustRange)

    noisyArray = array + noise

    return noisyArray, noise

def sinNoise (array, rate = 5000, frequency = 1.0, amplitude = 0.2):
    samples = np.linspace(0, 2 * np.pi, int(math.floor(rate / frequency)))

    print

    if samples.size < array.size:
        repetitions = int(np.floor(array.size/samples.size))

        samples = np.tile(samples, repetitions)
        samples = np.append(samples, samples[0:array.size - samples.size])
    elif samples.size > array.size:
        samples = samples[0:array.size]

    noise = amplitude * np.sin(samples)
    noisyArray = array + noise

    return noisyArray, noise
