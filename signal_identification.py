# 导入所需的库，例如numpy
import numpy as np

def identify_signal(preprocessed_signal):
    """
    识别预处理过的信号的类型。

    参数:
        preprocessed_signal (np.array): 预处理过的信号。

    返回:
        signal_type (str): 信号的类型，例如'AM', 'FM', 'CW', '2ASK', '2PSK', '2FSK'。
    """

    if np.max(preprocessed_signal) > 0.5:
        signal_type = 'AM'
    else:
        signal_type = 'Unknown'

    return signal_type
