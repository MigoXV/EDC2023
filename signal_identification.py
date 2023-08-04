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
from scipy.fftpack import fft, fftfreq,correlate

def is_cw(preprocessed_signal, fs=8e6, threshold=0.5):
    """
    函数的目的是识别信号是否为CW（AM或FM）或者数字调制（2ASK,2PSK,2FSK）
    参数：
    preprocessed_signal (numpy.ndarray): 输入信号
    fs (float): 采样频率
    threshold (float): 用来区分CW和数字信号的阈值

    返回值：
    bool: 如果信号为CW，返回True；如果为数字调制，返回False
    """

    # 使用快速傅里叶变换（FFT）得到频谱
    spectrum = np.abs(fft(preprocessed_signal))

    # 找到主导频率成分
    freq = fftfreq(len(preprocessed_signal), 1 / fs)
    dominant_freq = freq[np.argmax(spectrum)]

    # 归一化信号
    normalized_signal = preprocessed_signal / np.max(np.abs(preprocessed_signal))

    # 计算信号的自相关函数
    autocorr = correlate(normalized_signal, normalized_signal)

    # 如果信号是CW（AM或FM），它会在主频上有一个高峰，
    # 并且其自相关函数将是一个平滑的函数。
    # 如果信号是数字调制（2ASK, 2PSK, 2FSK），它会有突然的变化，
    # 这就导致在自相关函数中有高峰。
    # 因此，我们可以通过检查自相关函数的最大值与平均值的比例来确定信号类型
    if np.max(autocorr) / np.mean(autocorr) > threshold:
        return True  # 信号为CW
    else:
        return False  # 信号为数字调制

def identify_signal(preprocessed_signal, window_size=1000):

    flag_cw=is_cw(preprocessed_signal)

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
    return signal_type,flag_cw



if __name__=="__main__":
    data=np.loadtxt('data-am.dat')
    print(identify_signal(data))
    data=np.loadtxt('data-fm.dat')
    print(identify_signal(data))
