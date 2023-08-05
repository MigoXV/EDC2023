# 导入必要的库，例如 numpy
import numpy as np
import json
import matplotlib.pyplot as plt
# from scipy.fft import fft,fftfreq
import math
import signal_identification
import my_filter


def T_counter(demodulated_signal, signal_type):

    # 首先，去除直流分量
    demodulated_signal = demodulated_signal - np.mean(demodulated_signal)

    # 然后找到零点交叉
    crossings = np.where(np.diff(np.sign(demodulated_signal)))[0]

    # 由于噪声可能会导致错误的零点交叉，需要进一步处理
    # 例如，可以设置一个最小周期，用来过滤掉过小的周期（可能由噪声导致）
    min_period = 600  # 需要根据你的信号的具体频率和采样率来设定
    crossings_diff = np.diff(crossings)
    valid_crossings_diff = crossings_diff[crossings_diff > min_period]

    # 一个周期应该包含两个零点交叉（一个从正到负，一个从负到正）
    num_periods = len(valid_crossings_diff) / 2
    num_periods = math.ceil(num_periods)
    # if signal_type=='AM':
    #     num_periods=math.ceil(num_periods)
    # elif signal_type=='FM':
    #     num_periods=math.ceil(num_periods)
    return num_periods
    # print("The number of sine wave periods in the signal: ", num_periods)


def estimate_parameters(signal_type, demodulated_signal, preprocessed_signal):
    """
    根据预处理过的信号和它的类型估计信号的参数。

    参数:
        signal_type (str): 信号的类型，例如 'AM', 'FM', 'CW', '2ASK', '2PSK', '2FSK'。
        preprocessed_signal (np.array): 预处理过的信号。

    返回:
        params (dict): 一个包含参数名称和它们的估计值的字典。
    """

    with open('parameter.json', 'r', encoding='utf-8') as f:
        params = json.loads(f.read())
    # params = {}
    # if signal_type != 'CW' or signal_type != '2PSK':
    #     # 找到周期数
    #     T_num = T_counter(demodulated_signal, signal_type)
    #     params['T_num'] = T_num

    if signal_type == '2PSK':
        T_num=int(params['Rc']/2000)
    elif signal_type == 'CW':
        pass
    else:
        # 找到周期数
        T_num = T_counter(demodulated_signal, signal_type)
    
    params['T_num'] = T_num

    # 根据信号的类型来估计参数。
    # 这可能涉及到复杂的信号处理和机器学习技术，
    # 这些技术超出了这个例子的范围。

    if signal_type == 'AM' or signal_type == '2ASK' or signal_type == '2PSK' or signal_type == 'CW':
        signal_type_ensure = signal_type
    elif signal_type == 'FMor2FSK':
        signal_type_ensure = signal_identification.fm_or_2fsk_demodulated(
            demodulated_signal)
        
    params['type'] = signal_type_ensure

    if signal_type_ensure == 'AM':
        # 示例: 对于 'AM' 信号，我们可能会估计调幅系数 'ma'，
        # 这可以通过测量信号的峰峰值来简单地估计
        ma = 2*(np.max(demodulated_signal[200:7800]) - np.min(demodulated_signal[200:7800]))/(
            np.max(preprocessed_signal[200:7800]) - np.min(preprocessed_signal[200:7800]))
        ma = ma*1.2710863155094008252182992122047-0.3213175708408039188486140810474
        a = 1.6665867348459082
        b = -0.7583466975592283
        c = -1.4545079628726665
        d = 2.0646620477523925
        e = -0.19408674567914688
        ma = a * ma**4 + b * ma**3 + c * ma**2 + d * ma + e
        params['ma'] = ma
    elif signal_type_ensure == 'FM':
        # 对于 'FM' 信号，我们可能需要估计调频系数 'mf' 和最大频偏 'delta_f_max'
        # 这可能需要通过傅里叶变换或其他频率分析技术来实现
        # 这里我们只是用一个占位符来代替真实的估计值
        # params['mf'] = 0  # 占位符
        a0 = 2062.853052728227
        a1 = -3047.2164740322733
        a2 = 2657.804532001301
        a3 = -891.2749824438622
        a4 = 174.87221748314695
        a5 = -21.364206741121418
        a6 = 1.6694191837467751
        a7 = -0.08336759687893586
        a8 = 0.002571607130951519
        a9 = -4.461112018617971e-05
        a10 = 3.327529122326497e-07

        def tenth_degree_function(x, a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10):
            return a0 + a1*x + a2*x**2 + a3*x**3 + a4*x**4 + a5*x**5 + a6*x**6 + a7*x**7 + a8*x**8 + a9*x**9 + a10*x**10

        delta_f_max = tenth_degree_function(
            params['DFmax'], a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10)
        params['delta_f_max'] = delta_f_max  # 占位符

        filted_signal = my_filter.FM_filter_after(demodulated_signal)
        filted_signal[:89] = filted_signal[89]
        filted_signal[-90:] = filted_signal[-90]
        np.savetxt('result.dat', filted_signal)

    # 以此类推，对于其他类型的信号，我们也可以添加相应的参数估计代码...
    with open('parameter.json', 'w', encoding='UTF-8') as f:
        f.write(json.dumps(params))
    return params


if __name__ == "__main__":
    result = np.loadtxt('result.dat')
    # estimate_parameters('AM',result)
    # T_counter(results,signal_type)

# 75 {'ma': 0.8756927051634225}
# 100 {'ma': 0.9681466583590149}
# 50 ma: 0.7053361985235028
# 30 ma: 0.6543110802651244
