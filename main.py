# 导入必要的模块
# import signal_output


import signal_preprocessing
import signal_identification
import parameter_estimation
import signal_demodulation
import user_interface
import numpy as np
import matplotlib.pyplot as plt
import json

def main():
    params={}
    with open('parameter.json','w',encoding='UTF-8') as f:
        f.write(json.dumps(params))
    
    # 采样信号
    import signal_sampling #不采样调试时注释本行
    signal_sample = np.loadtxt("data.dat")

    # 预处理信号
    # preprocessed_signal = signal_preprocessing.preprocess_signal(signal_sample)
    preprocessed_signal=signal_sample
    # 识别信号类型
    signal_type,is_cw = signal_identification.identify_signal(preprocessed_signal)

    # print("信号类型为：",signal_type)


    # 解调信号
    demodulated_signal = signal_demodulation.demodulate_signal(signal_type,preprocessed_signal,is_cw)

    np.savetxt('result.dat',demodulated_signal)
    

    
    # 参数估计
    parameters = parameter_estimation.estimate_parameters(signal_type,demodulated_signal,preprocessed_signal,is_cw)

    # 显示结果
    user_interface.display_signal_info(signal_type, parameters)

    # 输出解调信号供示波器观测
    user_interface.output_signal()

    # 采样信号、解调信号绘图
    plt.figure()
    plt.plot(signal_sample)
    plt.savefig('data.png')
    plt.figure()
    plt.plot(demodulated_signal)
    plt.savefig('result.png')
    
    
if __name__ == "__main__":
    main()
