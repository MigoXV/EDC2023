import numpy as np
from scipy.signal import hilbert, fftconvolve
from scipy.fftpack import fft, fftfreq

def identify_modulation(data_file, window_size=1000):
    # 加载数据
    data = np.loadtxt(data_file)

    # 计算解析信号（希尔伯特变换）
    analytic_signal = hilbert(data)
    # 计算幅度包络和瞬时相位
    amplitude_envelope = np.abs(analytic_signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))

    # 计算瞬时频率（相位的导数）
    instantaneous_frequency = (np.diff(instantaneous_phase) / (2.0 * np.pi)) * 8e6

    # 计算信号的FFT
    yf = fft(data)
    xf = fftfreq(len(data), 1 / 8e6)

    # 计算幅度频谱
    amplitude_spectrum = 2.0 / len(data) * np.abs(yf[:len(data)//2])

    # 计算幅度包络的滑动窗口变化率
    amplitude_envelope_diff = np.std(fftconvolve(amplitude_envelope, np.ones(window_size), 'valid') / window_size)

    print('amplitude_envelope_diff:',amplitude_envelope_diff)
    print('np.mean(np.abs(instantaneous_frequency)):',np.mean(np.abs(instantaneous_frequency)))
    
    # 检查信号是AM还是FM
    if amplitude_envelope_diff > 0.005 and np.mean(np.abs(instantaneous_frequency)) < 2e6:
        print('信号是幅度调制（AM）。')
    elif amplitude_envelope_diff <= 0.005 and np.mean(np.abs(instantaneous_frequency)) >= 2e6:
        print('信号是频率调制（FM）。')
    else:
        print('信号不能明确地对应AM或FM调制。')

identify_modulation('data-am.dat')
