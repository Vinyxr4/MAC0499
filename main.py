# import audio.audioHandler as audio
# import supression.spectralSubtraction as specSub
# import supression.fastLMS as flms
# import noisy.noisy as noisy
# import tests.tests as test
# import numpy as np
# import multiprocessing as mp
# import matplotlib.pyplot as plt

# import supression.Plca as plca

# audio_path = 'audio_files'
# audios = ['history', 'die_hard']

# # testAudio = '{}/{}.wav'.format(audio_path, audios[1])

# audioArray, sampleRate2 = audio.getData('audio_files/echoPlanar.wav')
# audioArray2, sampleRate = audio.getData('audio_files/die_hard.wav')

# audioArray2 = audioArray2[:len(audioArray)]
# audioArray3 = [row[0] for row in audioArray]

# noiseTransf = np.fft.fft(audioArray3)
# audioTransf = np.fft.fft(audioArray2)

# resultantTransf = (noiseTransf + audioTransf)
# resultant = np.fft.ifft(resultantTransf).real

# resultant = ((resultant - np.min(resultant)) / (np.max(resultant) - np.min(resultant))) * 2 - 1.0

# audioNoiseNonNorm = audioArray3
# # audioArray3 = ((audioArray3 - np.min(audioArray3)) / (np.max(audioArray3) - np.min(audioArray3))) * 2 - 1.0

# teste = (0.5 * np.asarray(audioArray2)) + (0.5 * np.asarray(audioArray3))

# teste = ((teste - np.min(teste)) / (np.abs(np.min(teste)) + np.max(teste))) * 2 - 1.0

# testeTransf = np.fft.fft(teste)
# print(np.sum(np.abs(teste-audioNoiseNonNorm))/len(audioArray3))
# # print(np.abs(resultant - teste)[:100])

# # resultant = [row[0] for row in audioArray] + audioArray2

# # fig = plt.figure(figsize=(1, 2))

# # plt.subplot(1, 4, 1)
# # plt.plot(resultant)
# # plt.subplot(1, 4, 2)
# # plt.plot(teste)
# # plt.subplot(1, 4, 3)
# # plt.plot(audioArray2)
# # plt.subplot(1, 4, 4)
# # plt.plot(audioArray3)
# # plt.show()

# audio.saveAs(resultant, sampleRate, 'audio_files/echoPlanarDieHard.wav')
# audio.saveAs(audioArray2, sampleRate, 'audio_files/trimmedDieHard.wav')
# audio.saveAs(audioArray3, sampleRate, 'audio_files/echoPlanarMono.wav')
# # audioArray = audioArray[:22000]

# # totalSeconds = 1.0 * audioArray.size / sampleRate

# # instances = int(totalSeconds / 2)

# # suppressedAudio, noisyAudio, sampleRate, noise, elapsedTime = test.spectral(testAudio)
# # suppressedAudio, noisyAudio, sampleRate, noise, elapsedTime = test.fastlms(testAudio)

# # audio.saveAs(noise, sampleRate, 'pureNoise2.wav')

# # print(elapsedTime)

# # print('Noisy audio:')
# # # audio.play(noisyAudio, sampleRate)
# # audio.saveAs(noisyAudio, sampleRate, 'noisy2.wav')

# # print('Spectral supressed audio:')
# # audio.saveAs(suppressedAudio, sampleRate, 'test.wav')

# # # plca.plca(noisyAudio, sampleRate)

# # audio1, sample1 = audio.getData(('audio_files/echoPlanarDieHard.wav'))
# # audio2, sample2 = audio.getData(('sera.wav'))

# # # fig = plt.figure(figsize=(1, 2))

# # plt.subplot(1, 2, 1)
# # plt.plot(np.fft.fft(audio1))
# # plt.subplot(1, 2, 2)
# # plt.plot(np.fft.fft(audio2))
# # plt.show()