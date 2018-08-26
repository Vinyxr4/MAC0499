import numpy as np
import math

def plca(audioArray, sampleRate):
    transformedAudio = np.fft.fft(audioArray)

    print((freq * sampleRate)[0:100])

def update_priori_sz_given_f(priories_s, priories_z_given_s, priories_f_given_sz, s, z, f):
    dividend = np.zeros((s, z, f))

    for s_prime in range(s):
        for z_prime in range(z):
            for f_prime in range(f):
                dividend[s_prime][z_prime][f_prime] = priories_s[s_prime] * priories_z_given_s[s_prime][z_prime] * priories_f_given_sz[s_prime][z_prime][f_prime]
    
    divisor = np.zeros((f))
    
    for f_prime in range(f):
        for s_prime in range(len(priories_s)):
            inner_divisor = 0.0
            
            for z_prime in range(z):
                inner_divisor += priories_z_given_s[s_prime][z_prime] * priories_f_given_sz[s_prime][z_prime][f_prime]

            divisor[f_prime] += priories_s[s_prime] * inner_divisor
            
    epslon = 0.0
    result = dividend / divisor if divisor.all() > epslon else np.zeros((f))
    
    return result

def update_priori_s(priories_sz_given_f, spectrum, s, z, f):
    dividend = np.zeros((s))

    for s_prime in range(s):
        for f_prime in range(f):
            inner_dividend = 0.0
            
            for z_prime in range(z):
                inner_dividend += priories_sz_given_f[s_prime][z_prime][f_prime]

            dividend[s_prime] += spectrum[f_prime] * inner_dividend

    divisor = 0.0

    for s_prime in range(s):
        inner_divisor = 0.0

        for f_prime in range(f):
            inner_inner_divisor = 0.0
            
            for z_prime in range(z):
                inner_inner_divisor += priories_sz_given_f[s_prime][z_prime][f_prime]

            inner_divisor += spectrum[f_prime] * inner_inner_divisor

        divisor += inner_divisor

    epslon = 0.0
    result = np.zeros((s))
    
    result = dividend / divisor if divisor.any() > epslon else np.zeros((s))
    
    return result

def update_priori_z_given_s(priories_sz_given_f, spectrum, s, z):
    dividend = np.zeros((s, z))

    for s_prime in range(s):
        for z_prime in range(z):
            for f_prime in range(len(priories_sz_given_f[0][0])):
                dividend[s_prime][z_prime] += spectrum[f_prime] * priories_sz_given_f[s_prime][z_prime][f_prime]

    divisor = np.zeros((s))
    result = np.zeros((s, z))

    for s_prime in range(s):
        for f_prime in range(len(priories_sz_given_f[0][0])):
            inner_divisor = 0.0
            
            for z_prime in range(len(priories_sz_given_f[0])):
                inner_divisor += priories_sz_given_f[s_prime][z_prime][f_prime]

            divisor[s_prime] += spectrum[f_prime] * inner_divisor

        epslon = 0.0
        result[s_prime] = dividend[s_prime] / divisor[s_prime] if divisor[s_prime] > epslon else np.zeros(z)

    return result

def update_priori_f_given_sz(all_priories_sz_given_f, all_spectrums, s, z, f, turn):
    dividend = np.zeros((z, f))

    for z_prime in range(z):
        for f_prime in range(f):
            for t_prime in range(turn + 1):
                dividend[z_prime][f_prime] += all_spectrums[t_prime][f_prime] * all_priories_sz_given_f[t_prime][s][z_prime][f_prime]

    divisor = np.zeros((z))
    result = np.zeros((z, f))

    for z_prime in range(z):
        for f_prime in range(len(all_priories_sz_given_f[0][0][0])):
            inner_divisor = 0.0
            
            for t_prime in range(turn + 1):
                inner_divisor += all_priories_sz_given_f[t_prime][s][z_prime][f_prime] * all_spectrums[t_prime][f_prime]

            divisor[z_prime] += inner_divisor

        epslon = 0.0
        result[z_prime] = dividend[z_prime] / divisor[z_prime] if divisor.any() > epslon else np.zeros((f))

    return result

def test_first_update(s, z, f):
    priories_s = np.zeros((s))
    priories_z_given_s = np.zeros((s, z))
    priories_f_given_sz = np.zeros((s, z, f))

    priories_s[:] = 1.0 / s

    for s_prime in range(s):
        priories_z_given_s[s_prime][:] = 1.0 / z

        for z_prime in range(z):
            priories_f_given_sz[s_prime][z_prime][:] = 1.0 / f

    val = update_priori_sz_given_f(priories_s, priories_z_given_s, priories_f_given_sz, s, z, f)

    print (val)

def test_second_update(s, z, f):
    priories_sz_given_f = np.zeros((s, z, f))

    spectrum = np.zeros((f))

    spectrum[:] = 1.0 / f

    for s_prime in range(s):
        for z_prime in range(z):
            priories_sz_given_f[s_prime][z_prime][:] = 1.0 / f

    val = update_priori_s(priories_sz_given_f, spectrum, s)

    print (val)

def test_third_update(s, z, f):
    priories_sz_given_f = np.zeros((s, z, f))

    spectrum = np.zeros((f))

    spectrum[:] = 1.0 / f

    for s_prime in range(s):
        for z_prime in range(z):
            priories_sz_given_f[s_prime][z_prime][:] = 1.0 / f

    val = update_priori_z_given_s(priories_sz_given_f, spectrum, s, z)

    print (val)

def test_fourth_update(s, z, f, turns):
    all_priories_sz_given_f = np.zeros((turns, s, z, f))
    all_spectrums = np.zeros((turns, f))
    priories_s = np.zeros((s))
    priories_z_given_s = np.zeros((s, z))
    priories_f_given_sz = np.zeros((s, z, f))

    priories_s[:] = 1.0 / s
    
    for z_prime in range(z):
        priories_f_given_sz[0][z_prime][:] = 1.0 / f
        # priories_f_given_sz[1][z_prime][:] = 1.0 / f

    # priories_f_given_sz[0][0][0] = (2.0/3) * f
    # priories_f_given_sz[0][0][1] = (1.0/3) * f

    for s_prime in range(s):
        priories_z_given_s[s_prime][:] = 1.0 / z

    for t_prime in range(turns):
        # all_spectrums[t_prime][:] = 1.0 / f
        all_spectrums[t_prime][0] = 3
        all_spectrums[t_prime][1] = 5
        all_spectrums[t_prime][2] = 2
    
        for s_prime in range(s):
            for z_prime in range(z):
                all_priories_sz_given_f[t_prime][s_prime][z_prime][:] = 1.0 / f

    # val = update_priori_f_given_sz(all_priories_sz_given_f, all_spectrums, 0, z, f, 0)
    # print(val)
    
    # print('Results at turn -1:')
    # print (all_priories_sz_given_f[0])
    # print (priories_s)
    # print (priories_z_given_s)
    # print (priories_f_given_sz[0])
    # print('****')

    for t_prime in range(turns):
        all_priories_sz_given_f[t_prime] = update_priori_sz_given_f(priories_s, priories_z_given_s, priories_f_given_sz, s, z , f)
        priories_s = update_priori_s(all_priories_sz_given_f[t_prime], all_spectrums[t_prime], s, z, f)
        priories_z_given_s = update_priori_z_given_s(all_priories_sz_given_f[t_prime], all_spectrums[t_prime], s, z)
        priories_f_given_sz[0] = update_priori_f_given_sz(all_priories_sz_given_f, all_spectrums, 0, z, f, t_prime)
        priories_f_given_sz[1] = update_priori_f_given_sz(all_priories_sz_given_f, all_spectrums, 1, z, f, t_prime)

        # print('Results at turn {}:').format(t_prime)
        # print (all_priories_sz_given_f[t_prime])
        # print (priories_s)
        # print (priories_z_given_s)
        # print (priories_f_given_sz[0])
        # print('****')

    # print (priories_f_given_sz[0])
    # print (priories_f_given_sz[1])

# test_first_update(2, 2, 2)
# test_second_update(10, 1, 1)
# test_third_update(2, 10, 10)
# test_fourth_update(2, 2, 3, 2)
