import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz


# 设计低通滤波器
def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# 设置滤波器参数
cutoff_frequency = 2*10e6  # 截止频率
order = 6  # 滤波器阶数

# 应用低通滤波器
filtered_signal = butter_lowpass_filter(signal, cutoff_frequency, fs, order)


