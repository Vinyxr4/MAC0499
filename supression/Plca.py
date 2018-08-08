import numpy as np
import math

def plca(audioArray, sampleRate):
    transformedAudio = np.fft.fft(audioArray)

    print((freq * sampleRate)[0:100])

def update_priori_sz_given_f(priories_s, priories_z_given_s, priories_f_given_sz, s, z, f):
    dividend = priories_s[s] * priories_z_given_s[s][z] * priories_f_given_sz[s][z][f]

    divisor = 0.0

    for s_prime in range(len(priories_s)):
        inner_divisor = 0.0
        
        for z_prime in range(len(priories_z_given_s[0])):
            inner_divisor += priories_z_given_s[s_prime][z_prime] * priories_f_given_sz[s_prime][z_prime][f]

        divisor += priories_s[s_prime]  * inner_divisor
    
    epslon = 0.0
    result = dividend / divisor if divisor > epslon else 0.0

    return result

def update_priori_s(priories_sz_given_f, spectrum, s):
    dividend = 0.0

    for f_prime in range(len(priories_sz_given_f[0][0])):
        inner_dividend = 0.0
        
        for z_prime in range(len(priories_sz_given_f[0])):
            inner_dividend += priories_sz_given_f[s][z_prime][f_prime]

        dividend += spectrum[f_prime] * inner_dividend

    divisor = 0.0

    for s_prime in range(len(priories_sz_given_f)):
        inner_divisor = 0.0

        for f_prime in range(len(priories_sz_given_f[0][0])):
            inner_inner_divisor = 0.0
            
            for z_prime in range(len(priories_sz_given_f[0])):
                inner_inner_divisor += priories_sz_given_f[s_prime][z_prime][f_prime]

            inner_divisor += spectrum[f_prime] * inner_inner_divisor

        divisor += inner_divisor

    epslon = 0.0
    result = dividend / divisor if divisor > epslon else 0.0

    return result

def test_first_update(s, z, f, iterations):
    priories_s = np.zeros((s))
    priories_z_given_s = np.zeros((s, z))
    priories_f_given_sz = np.zeros((s, z, f))

    priories_s[:] = 1.0 / s

    for s_prime in range(s):
        priories_z_given_s[s_prime][:] = 1.0 / z

        for z_prime in range(z):
            priories_f_given_sz[s_prime][z_prime][:] = 1.0 / f

    val = update_priori_sz_given_f(priories_s, priories_z_given_s, priories_f_given_sz, 0, 0, 0)

    print (val)

def test_second_update(s, z, f, iterations):
    priories_sz_given_f = np.zeros((s, z, f))

    spectrum = np.zeros((f))

    spectrum[:] = 1.0 / f

    for s_prime in range(s):
        for z_prime in range(z):
            priories_sz_given_f[s_prime][z_prime][:] = 1.0 / f

    val = update_priori_s(priories_sz_given_f, spectrum, 0)

    print (val)

# test_first_update(2, 3, 1, 10)
# test_second_update(2, 1, 1, 10)
