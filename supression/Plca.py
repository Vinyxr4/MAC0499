import numpy as np
import pywt
import time

def plca(audioArray, noiseArray, iterations):
    startTime = time.time()
    
    usedAudio = np.copy(audioArray)
    usedNoise = np.copy(noiseArray)
    
    usedAudio[:] += 1
    usedAudio[:] *= 0.5
    usedNoise[:] += 1
    usedNoise[:] *= 0.5

    suppressedArray = fixed_plca(2, 10, len(audioArray), iterations, usedNoise, usedAudio)

    suppressedArray[:] *= 2
    suppressedArray[:] -= 1

    maxLevel = pywt.dwt_max_level(len(noiseArray), 'db8')

    noiseDecomp = pywt.wavedec(noiseArray, 'db8', level=maxLevel)
    noisyDecomp = pywt.wavedec(audioArray, 'db8', level=maxLevel)
    obtainedDecomp = pywt.wavedec(suppressedArray, 'db8', level=maxLevel)

    for i in range(len(noiseDecomp)):
        var = np.var(noiseDecomp[i])
        noisyVar = np.var(noisyDecomp[i])

        epslon = np.sqrt(noisyVar / var)
        log = np.log(np.sqrt(1 + (1.0/epslon)))
        root = np.sqrt(2 * (epslon + (epslon ** 2)) * log)

        threshold = (var / epslon) * root

        obtainedDecomp[i] = pywt.threshold(obtainedDecomp[i], threshold)

    recovered = pywt.waverec(obtainedDecomp, 'db8')

    elapsedTime = time.time() - startTime

    return recovered, noiseArray, elapsedTime

def update_priori_sz_given_f(priories_s, priories_z_given_s, priories_f_given_sz, s, z, f):
    dividend = np.zeros((s, z, f))

    for s_prime in range(s):
        for z_prime in range(z):
            dividend[s_prime][z_prime] = priories_s[s_prime] * priories_z_given_s[s_prime][z_prime] * priories_f_given_sz[s_prime][z_prime]
    
    divisor = np.zeros((f))
    
    for s_prime in range(len(priories_s)):
        inner_divisor = np.zeros(f)
        
        for z_prime in range(z):
            inner_divisor += priories_z_given_s[s_prime][z_prime] * priories_f_given_sz[s_prime][z_prime]

        divisor += priories_s[s_prime] * inner_divisor
            
    epslon = 0.0
    result = dividend / divisor if divisor.all() > epslon else np.zeros((f))
    
    return result

def update_priori_s(priories_sz_given_f, spectrum, s, z, f):
    dividend = np.zeros((s))
    
    dividend[:] = np.sum(spectrum * priories_sz_given_f[:])
    divisor = np.sum(spectrum * priories_sz_given_f)

    epslon = 0.0
    
    result = dividend / divisor if divisor.any() > epslon else np.zeros((s))
    
    return result

def update_priori_z_given_s(priories_sz_given_f, spectrum, s, z):
    dividend = np.zeros((s, z))

    for s_prime in range(s):
        for z_prime in range(z):
            dividend[s_prime][z_prime] += np.sum(spectrum * priories_sz_given_f[s_prime][z_prime])

    divisor = np.zeros((s))
    divisor[:] = np.sum(spectrum * priories_sz_given_f[:])
    
    epslon = 0.0
    result = np.zeros((s, z))
    for s_prime in range(s):
        result[s_prime] = dividend[s_prime] / divisor[s_prime] if divisor[s_prime] > epslon else np.zeros(z)

    return result

def update_priori_f_given_sz(all_priories_sz_given_f, all_spectrums, s, z, f, turn):
    dividend = np.zeros((z, f))

    for z_prime in range(z):
        for t_prime in range(turn + 1):
            dividend[z_prime] += all_spectrums[t_prime] * all_priories_sz_given_f[t_prime][s][z_prime]

    divisor = np.zeros((z))
    result = np.zeros((z, f))

    for z_prime in range(z):
        inner_divisor = np.zeros(len(all_priories_sz_given_f[0][0][0]))
        
        for t_prime in range(turn + 1):
            inner_divisor += all_priories_sz_given_f[t_prime][s][z_prime] * all_spectrums[t_prime]

        divisor[z_prime] += np.sum(inner_divisor)

        epslon = 0.0
        result[z_prime] = dividend[z_prime] / divisor[z_prime] if divisor.any() > epslon else np.zeros((f))

    return result

def fixed_plca(s, z, f, turns, noise, audioArray):
    all_priories_sz_given_f = np.zeros((turns, s, z, f))
    noises = np.zeros((turns, f))
    audios = np.zeros((turns, f))
    priories_s = np.zeros((s))
    priories_z_given_s = np.zeros((s, z))
    priories_f_given_sz = np.zeros((s, z, f))

    priories_s[:] = 1.0 / s
    
    for z_prime in range(z):
        priories_f_given_sz[0][z_prime][:] = 1.0 / f

    for s_prime in range(s):
        priories_z_given_s[s_prime][:] = 1.0 / z

    for t_prime in range(turns):
        noises[t_prime] = noise
        audios[t_prime] = audioArray
    
        for s_prime in range(s):
            for z_prime in range(z):
                all_priories_sz_given_f[t_prime][s_prime][z_prime][:] = 1.0 / f

    priories_s = update_priori_s(all_priories_sz_given_f[t_prime], noises[t_prime], s, z, f)
    priories_z_given_s = update_priori_z_given_s(all_priories_sz_given_f[t_prime], noises[t_prime], s, z)
    all_priories_sz_given_f[t_prime] = update_priori_sz_given_f(priories_s, priories_z_given_s, priories_f_given_sz, s, z , f)
    priories_f_given_sz[0] = update_priori_f_given_sz(all_priories_sz_given_f, noises, 0, z, f, t_prime)

    priories_s[:] = 1.0 / s

    for s_prime in range(s):
        priories_z_given_s[s_prime][:] = 1.0 / z

    for t_prime in range(turns):
        for s_prime in range(s):
            for z_prime in range(z):
                all_priories_sz_given_f[t_prime][s_prime][z_prime][:] = 1.0 / f

    for z_prime in range(z):
        priories_f_given_sz[1][z_prime][:] = 1.0 / f

    for t_prime in range(turns):
        priories_s = update_priori_s(all_priories_sz_given_f[t_prime], audios[t_prime], s, z, f)
        priories_z_given_s = update_priori_z_given_s(all_priories_sz_given_f[t_prime], audios[t_prime], s, z)
        all_priories_sz_given_f[t_prime] = update_priori_sz_given_f(priories_s, priories_z_given_s, priories_f_given_sz, s, z , f)
        priories_f_given_sz[1] = update_priori_f_given_sz(all_priories_sz_given_f, audios, 1, z, f, t_prime)

    t = np.zeros(f)
    for i in range(z):
        t += all_priories_sz_given_f[turns-1][1][i][:]

    return t
