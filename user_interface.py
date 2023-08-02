# 导入必要的库
import matplotlib.pyplot as plt
import numpy as np

def plot_demodulated_signal(demodulated_signal, signal_type):
    """
    将解调后的信号用matplotlib.pyplot画出。

    参数:
        demodulated_signal (np.array): 解调后的信号。
        signal_type (str): 信号的类型。

    返回:
        None
    """

    # 创建一个新的图形
    plt.figure()

    # 绘制解调后的信号
    plt.plot(demodulated_signal)

    # 设置图形的标题
    plt.title(f'Demodulated signal of type {signal_type}')

    # 设置图形的x轴标签
    plt.xlabel('n')

    # 设置图形的y轴标签
    plt.ylabel('Amplitude')

    # 显示图形
    plt.show()

def display_signal_info(signal_type, signal_params):
    """
    将信号的信息打印到控制台。

    参数:
        signal_type (str): 信号的类型。
        signal_params (dict): 信号的参数。

    返回:
        None
    """

    print(f'Signal type: {signal_type}')

    for param_name, param_value in signal_params.items():
        print(f'{param_name}: {param_value}')
        
def display_results():
    pass

def output_signal():
    import signal_output

if __name__=="__main__":
    n=np.array(range(1000))/1000
    a=np.sin(n*2*np.pi)
    plot_demodulated_signal(a,'test wave')
