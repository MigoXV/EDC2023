# 导入必要的库，例如 numpy
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert
import my_filter

def am_demodulation(modulated_wave):
    # 使用希尔伯特转换找到解析信号
    analytic_signal = hilbert(modulated_wave)
    # 计算解析信号的绝对值，得到解调信号
    envelope = np.abs(analytic_signal)

    return envelope

def fm_demodulation(data):
    fc=2e6
    fs=8e6

    t = np.arange(len(data)) / fs

    # 使用希尔伯特变换得到解析信号
    analytic_signal = hilbert(data)

    # 计算相位，然后对其进行解包
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))

    # 对相位进行差分，并考虑采样时间得到频率偏移
    frequency_deviation = np.diff(instantaneous_phase) / (2.0*np.pi) * 8e6
    
    frequency_deviation=np.append(frequency_deviation,frequency_deviation[-1])
    
    # FM信号的载波频率为2MHz，得到基带信号
    baseband = frequency_deviation - 2e6
    
    baseband=baseband/np.max(baseband[2000:6000])
    
    return baseband

def cw_demodulation():
    pass

def ask_demodulation():
    pass

def fsk_demodulation():
    pass

def psk_demodulation():
    pass

def demodulate_signal(signal_type, preprocessed_signal):
    """
    根据预处理过的信号和它的类型解调信号。

    参数:
        signal_type (str): 信号的类型，例如 'AM', 'FM', 'CW', '2ASK', '2PSK', '2FSK'。
        preprocessed_signal (np.array): 预处理过的信号。

    返回:
        demodulated_signal (np.array): 解调后的信号。
    """
    # 初始化一个空的 numpy array 来保存解调后的信号
    demodulated_signal = np.array([])

    # 根据信号的类型来解调信号。
    # 这可能涉及到复杂的信号处理和机器学习技术，
    # 这些技术超出了这个例子的范围。

    if signal_type == 'AM':

        demodulated_signal = am_demodulation(preprocessed_signal)
        filted_signal = my_filter.AM_filter_after(demodulated_signal)
        return filted_signal
        

    elif signal_type == 'FM':
        # 对于 'FM' 信号，我们可能需要进行更复杂的解调过程
        # 这可能需要通过傅里叶变换或其他频率分析技术来实现
        # 这里我们只是用一个占位符来代替真实的解调信号
        demodulated_signal = fm_demodulation(preprocessed_signal)
        filted_signal = my_filter.FM_filter_after(demodulated_signal)
        filted_signal[:39] = filted_signal[39]
        filted_signal[-40:] = filted_signal[-40]
        return filted_signal
    # 以此类推，对于其他类型的信号，我们也可以添加相应的解调代码...

    return demodulated_signal

if __name__=="__main__":
    data=np.loadtxt('data.dat')
    result=demodulate_signal('FM',data)
    
    plt.plot(result)
    plt.show()
    np.savetxt('result.dat',result)
 


