import numpy as np
import math
import time

def fastLms(signalInput, desiredOutput, M, step=0.1, forgetness=0.9):
    blocks = int(math.ceil(1.0 * signalInput.size/M))
    coefficients = np.random.rand(2*M)
    P = np.ones(2*M)
    totalOut = []

    startTime = time.time()

    for i in range(blocks):
        des = desiredOutput[i*M:(i+1)*M]
        
        if (des.size < M):
            des = np.append(des, np.random.rand(M-des.size))
        
        inp = []
        remaining = signalInput.size - (i-1)*M
        if i == 0:
            padding = np.zeros(M)
            inp = np.append(padding, signalInput[:M])
        elif remaining < 2*M:
            padding = np.zeros(2*M-remaining)
            inp = np.append(signalInput[(i-1)*M:], padding)
        else:
            inp = signalInput[(i-1)*M:(i+1)*M]
        
        block = flmsBlock(inp, des, coefficients, M, i, P)
        output, coefficients, P = flmsChunk(block, step, forgetness)

        totalOut.append(output)

    totalOut = np.asarray(totalOut).ravel()[:signalInput.size] 
    elapsed = time.time() - startTime

    return totalOut, elapsed

class flmsBlock(object):
    inBlk = []
    outBlk = []
    desiredOutBlk = []
    W = []
    filterLen = 0
    idx = 0
    pwr = []

    def __init__(self, inputBlk, desiredOutBlk, coefficients, filterLen, idx, pwr):
        self.inBlk = inputBlk
        self.desiredOutBlk = desiredOutBlk
        self.W = coefficients
        self.filterLen = filterLen
        self.idx = idx
        self.pwr = pwr

def flmsChunk(block, step, forgetness):
    U = np.fft.fft(block.inBlk)
    UH = conjugateUpdate(U)

    signalOutput = outputUpdate(U, block.W, block.filterLen)
    error = errorUpdate(block.desiredOutBlk, signalOutput, block.filterLen)
    P, D = updatePow(block.pwr, U, forgetness)
    constraint = gradientConstraint(error, UH, D, block.filterLen)
    
    coefficients = coeffUpdate(constraint, block.W, step)
    return np.real(signalOutput), coefficients, P

def gradientConstraint (error, UH, D, M):
    convolution = D * UH * error
    invConvolution = np.fft.ifft(convolution)

    paddedInv = np.append(invConvolution[:M], np.zeros(M))
    
    return np.fft.fft(paddedInv)

def coeffUpdate (constrain, coefficients, step):
    convolution = step * constrain
    update = convolution + coefficients

    return update

def errorUpdate (desiredBlock, outputBlock, M):
    if (desiredBlock.size != outputBlock.size):
        print(desiredBlock.size, outputBlock.size)

    error = desiredBlock - outputBlock

    paddedError = np.append(np.zeros(M), error)
    return np.fft.fft(paddedError)

def outputUpdate (matrixU, coefficients, M):
    convolution = matrixU * coefficients
    invConvolution = np.fft.ifft(convolution)

    return (invConvolution[M:2*M])

def conjugateUpdate (U):
    return np.conj(U)

def updatePow(P, U, gamma):
    P = gamma * P + (1 - gamma) * np.abs(U)**2
    D = 1 / P

    return P, D
