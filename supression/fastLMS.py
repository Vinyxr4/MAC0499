import numpy as np

def flms(signalInput, signalOutput, desiredOutput, M):
    U = kthMatrixFromInput(signalInput, M=M*2, k=1)
    UH = conjugateUpdate(U)

    coefficients = np.random.rand(2*M)

    error = errorUpdate(desiredOutput, signalOutput, M=M)
    
    constraint = gradientConstraint(error, UH, M)
    
    signalOutput = outputUpdate(U, coefficients, M)
    
    coefficients = coeffUpdate(constraint, coefficients, step=0.5)
    
    return signalOutput

def gradientConstraint (error, UH, M=30):
    error = error.reshape(2*M, 1)

    convolution = np.dot(UH, error)
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
    convolution = np.dot(matrixU, coefficients)

    invConvolution = np.fft.ifft(convolution)

    return np.real(invConvolution[M:2*M])

def conjugateUpdate (matrixU):
    return np.conj(matrixU)
