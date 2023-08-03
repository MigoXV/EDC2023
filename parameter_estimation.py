# 导入必要的库，例如 numpy
import numpy as np

def estimate_parameters(signal_type, demodulated_signal,preprocessed_signal):
    """
    根据预处理过的信号和它的类型估计信号的参数。

    参数:
        signal_type (str): 信号的类型，例如 'AM', 'FM', 'CW', '2ASK', '2PSK', '2FSK'。
        preprocessed_signal (np.array): 预处理过的信号。

    返回:
        params (dict): 一个包含参数名称和它们的估计值的字典。
    """
    params = {}

    # 根据信号的类型来估计参数。
    # 这可能涉及到复杂的信号处理和机器学习技术，
    # 这些技术超出了这个例子的范围。

    if signal_type == 'AM':
        # 示例: 对于 'AM' 信号，我们可能会估计调幅系数 'ma'，
        # 这可以通过测量信号的峰峰值来简单地估计
        params['ma'] = 2*(np.max(demodulated_signal[200:7800]) - np.min(demodulated_signal[200:7800]))/(np.max(preprocessed_signal[200:7800]) - np.min(preprocessed_signal[200:7800]))
        params['ma'] = params['ma']*1.2710863155094008252182992122047-0.3213175708408039188486140810474

    elif signal_type == 'FM':
        # 对于 'FM' 信号，我们可能需要估计调频系数 'mf' 和最大频偏 'delta_f_max'
        # 这可能需要通过傅里叶变换或其他频率分析技术来实现
        # 这里我们只是用一个占位符来代替真实的估计值
        params['mf'] = 0  # 占位符
        params['delta_f_max'] = 0  # 占位符

    # 以此类推，对于其他类型的信号，我们也可以添加相应的参数估计代码...

    return params

if __name__ == "__main__":
    result=np.loadtxt('result.dat')
    estimate_parameters('AM',result)
    
# 75 {'ma': 0.8756927051634225}
# 100 {'ma': 0.9681466583590149}
# 50 ma: 0.7053361985235028
# 30 ma: 0.6543110802651244    