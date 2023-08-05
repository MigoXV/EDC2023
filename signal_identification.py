import numpy as np
from scipy.signal import hilbert, fftconvolve
from scipy.fftpack import fft, fftfreq
import matplotlib.pyplot as plt

def get_phase_diff_std(preprocessed_signal):
    
    phase_diff_std=0
    
    # 计算希尔伯特变换
    analytic_signal = hilbert(preprocessed_signal)
    
    # 计算相位
    phase = np.unwrap(np.angle(analytic_signal))
    
    # 计算相位差
    phase_diff = np.diff(phase)
    
    # 对于一个单一载波信号，相位差应该是恒定的，我们可以通过检查相位差的标准差来看是否存在调制
    phase_diff_std = np.std(phase_diff)

    return phase_diff_std

def is_cw(preprocessed_signal, fs=8e6, carrier_freq=2e6):
    """
    判断输入的信号是否为单一载波信号。
    参数：
        preprocessed_signal: ndarray，需要判断的信号。
        fs: float，采样频率，单位Hz。
        carrier_freq: float，载波频率，单位Hz。
    返回值：
        bool，如果输入的信号是单一载波信号，返回True，否则返回False。
    """
    threshold=0.105
    fft_data=np.fft.fft(preprocessed_signal)
    fft_data_abs=abs(fft_data)
    fft_data_abs_normalized=fft_data_abs/np.sum(fft_data_abs)
    if np.max(fft_data_abs_normalized)>threshold:
        return True
    return False
    

def identify_signal(preprocessed_signal, window_size=1000):

    # 首先检查信号是经过调制的信号还是单纯的载波信号
    if is_cw(preprocessed_signal):
        return 'CW'
    
    #如果经过了调制运行下面的代码:

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

    # print('amplitude_envelope_diff:',amplitude_envelope_diff)
    # print('np.mean(np.abs(instantaneous_frequency)):',np.mean(np.abs(instantaneous_frequency)))
    
    # 检查信号是AM还是FM
    # if amplitude_envelope_diff > 0.001 and np.mean(np.abs(instantaneous_frequency)) < 2e6:
    if amplitude_envelope_diff > 0.001 and np.mean(np.abs(instantaneous_frequency)) >= 1.8e6:
        # print('信号是幅度调制（AM）。')
        signal_type='AM'
    elif amplitude_envelope_diff <= 0.001 and np.mean(np.abs(instantaneous_frequency)) >= 2e6:
        # print('信号是频率调制（FM）。')
        phase_diff_std=get_phase_diff_std(preprocessed_signal)
        
        # print('phase_diff_std=',phase_diff_std)

        if phase_diff_std<0.075:
            signal_type='FMor2FSK'
        else:
            signal_type='2PSK'
    elif np.mean(np.abs(instantaneous_frequency)) <= 1.8e6:
        signal_type='2ASK'
    else:
        # print('信号不能明确地对应AM或FM调制。')
        signal_type='unknown'
    return signal_type

def fm_or_2fsk_demodulated(demodulated_signal):
    # 对信号进行一阶差分
    diff_signal = np.diff(demodulated_signal)

    # 计算一阶差分的绝对值
    abs_diff_signal = np.abs(diff_signal)

    
    # plt.plot(abs_diff_signal)
    # plt.title('abs_diff_signal')
    # plt.ylim([0,0.015])
    # plt.show()
    # 设置一个阈值，大于这个阈值则认为是方波，否则是正弦波
    # 这个阈值可以通过对已知的正弦波和方波信号进行实验得到，这里假设是0.5
    threshold = 0.010

    # # 计算超过阈值的元素的比例
    # ratio = np.sum(abs_diff_signal > threshold) / len(abs_diff_signal)
    # print('ratio:',ratio)

    # 如果超过阈值的元素比例超过一半，则认为是方波
    if np.max(abs_diff_signal)>threshold:
        return '2FSK'
    else:
        return 'FM'
    
def type_ensure():
    pass

if __name__=="__main__":
    data=np.loadtxt('data-am.dat')
    print(identify_signal(data))
    data=np.loadtxt('data-fm.dat')
    
    

