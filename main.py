# 导入必要的模块
# import signal_output


import signal_preprocessing
import signal_identification
import parameter_estimation
import signal_demodulation
import user_interface
import numpy as np
import matplotlib.pyplot as plt

def main():
    # 采样信号
    import signal_sampling
    signal_sample = np.loadtxt("data.dat")

    # 预处理信号
    preprocessed_signal = signal_preprocessing.preprocess_signal(signal_sample)

    # 识别信号类型
    signal_type = signal_identification.identify_signal(preprocessed_signal)

    print("信号类型为：",signal_type)


    # 解调信号
    demodulated_signal = signal_demodulation.demodulate_signal(signal_type,preprocessed_signal)

    np.savetxt('result.dat',demodulated_signal)
    plt.plot(demodulated_signal)
    plt.savefig('result.png')
    
    # 参数估计
    parameters = parameter_estimation.estimate_parameters(signal_type,demodulated_signal,preprocessed_signal)
    
    # 显示结果
    user_interface.display_signal_info(signal_type, parameters)

    # 输出解调信号供示波器观测
    user_interface.output_signal()

    
    
if __name__ == "__main__":
    main()
