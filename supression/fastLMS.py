import numpy as np
import math

def FLMS(signalInput, desiredOutput, M):
    blocks = int(math.ceil(1.0 * signalInput.size/M))
    outputBlock = signalInput[:M]
    res = []
    coefficients = np.zeros(2*M)

    for i in range(blocks):
        inp = []
        des = []
        remaining = signalInput.size - (i-1)*M
        if i == 0:
            padding = np.zeros(M)
            inp = np.append(padding, signalInput[:M])
        elif remaining < 2*M:
            padding = np.zeros(2*M-remaining)
            inp = np.append(signalInput[(i-1)*M:], padding)
        else:
            inp = signalInput[(i-1)*M:(i+1)*M]

        des = desiredOutput[i*M:(i+1)*M]

        outputBlock, coefficients = flms(inp, outputBlock, des, coefficients, M, i)
        res.append(outputBlock)

    return np.asarray(res).ravel()[:signalInput.size]

def flms(signalInput, signalOutput, desiredOutput, coefficients, M, k):
    # U = kthMatrixFromInput(signalInput, M=M*2, k=k)
    
    U = np.fft.fft(signalInput)
    
    UH = conjugateUpdate(U)

    signalOutput = outputUpdate(U, coefficients, M)
    error = errorUpdate(desiredOutput, signalOutput, M=M)
    print(np.abs(np.fft.ifft(error)))
    constraint = gradientConstraint(error, UH, M)
    
    coefficients = coeffUpdate(constraint, coefficients, step=0.1)
    # print(coefficients)
    return signalOutput, coefficients

def gradientConstraint (error, UH, M=30):
    convolution = UH * error
    invConvolution = np.fft.ifft(convolution)
    
    padding = np.zeros(M)
    invFirstHalf = invConvolution[:M]

    paddedInv = np.append(invFirstHalf, padding)
    
    return np.fft.fft(paddedInv)

def coeffUpdate (constrain, coefficients, step=0.1):
    convolution = step * constrain
    update = convolution + coefficients

    return update

def errorUpdate (desiredBlock, outputBlock, M=30):
    error = desiredBlock - outputBlock

    padding = np.zeros(M)
    paddedError = np.append(padding, error)

    return np.fft.fft(paddedError)

def kthMatrixFromInput(input, M=30, k=1):
    matrix = []

    #k>=1
    for i in range(M):
        offset = k * M + i
        row = (input[offset - M + 1:offset + 1])[::-1]
        matrix.append(row)

    matrix = np.asarray(matrix)

    return np.fft.fftn(matrix, axes=(0,1)) 

def outputUpdate (matrixU, coefficients, M):
    convolution = matrixU * coefficients

    invConvolution = np.fft.ifft(convolution)

    return np.real(invConvolution[M:2*M])

def conjugateUpdate (matrixU):
    return np.conj(matrixU)
