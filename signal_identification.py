# # 导入所需的库，例如numpy
# import numpy as np

# def identify_signal(preprocessed_signal):
#     """
#     识别预处理过的信号的类型。

#     参数:
#         preprocessed_signal (np.array): 预处理过的信号。

#     返回:
#         signal_type (str): 信号的类型，例如'AM', 'FM', 'CW', '2ASK', '2PSK', '2FSK'。
#     """

#     if np.max(preprocessed_signal) > 0.5:
#         signal_type = 'AM'
#     else:
#         signal_type = 'Unknown'

#     return signal_type


import numpy as np
from scipy.signal import hilbert, fftconvolve
from scipy.fftpack import fft, fftfreq

def identify_signal(preprocessed_signal, window_size=1000):

    # 计算解析信号（希尔伯特变换）
    analytic_signal = hilbert(preprocessed_signal)
    # 计算幅度包络和瞬时相位
    amplitude_envelope = np.abs(analytic_signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))

    # 计算瞬时频率（相位的导数）
    instantaneous_frequency = (np.diff(instantaneous_phase) / (2.0 * np.pi)) * 8e6

    # 计算信号的FFT
    yf = fft(preprocessed_signal)
    xf = fftfreq(len(preprocessed_signal), 1 / 8e6)

    # 计算幅度频谱
    # amplitude_spectrum = 2.0 / len(preprocessed_signal) * np.abs(yf[:len(preprocessed_signal)//2])

    # 计算幅度包络的滑动窗口变化率
    amplitude_envelope_diff = np.std(fftconvolve(amplitude_envelope, np.ones(window_size), 'valid') / window_size)

    print('amplitude_envelope_diff:',amplitude_envelope_diff)
    print('np.mean(np.abs(instantaneous_frequency)):',np.mean(np.abs(instantaneous_frequency)))
    
    # 检查信号是AM还是FM
    # if amplitude_envelope_diff > 0.001 and np.mean(np.abs(instantaneous_frequency)) < 2e6:
    if amplitude_envelope_diff > 0.001:
        # print('信号是幅度调制（AM）。')
        signal_type='AM'
    elif amplitude_envelope_diff <= 0.001 and np.mean(np.abs(instantaneous_frequency)) >= 2e6:
        # print('信号是频率调制（FM）。')
        signal_type='FM'
    else:
        # print('信号不能明确地对应AM或FM调制。')
        signal_type='unknown'
    return signal_type

if __name__=="__main__":
    data=np.loadtxt('data-am.dat')
    print(identify_signal(data))
    data=np.loadtxt('data-fm.dat')
    print(identify_signal(data))
