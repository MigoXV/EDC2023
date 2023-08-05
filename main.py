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
import signal_IO

def main():
    params={}
    with open('parameter.json','w',encoding='UTF-8') as f:
        f.write(json.dumps(params))
    # while True:
        
    # 初始化设备
    signal_IO.initialize_device()
    
    # 采样信号
    signal_sample=signal_IO.signal_sampling()

    # 预处理信号
    # preprocessed_signal = signal_preprocessing.preprocess_signal(signal_sample)
    preprocessed_signal=signal_sample
    
    # 识别信号类型
    signal_type = signal_identification.identify_signal(preprocessed_signal)

    # 解调信号
    demodulated_signal = signal_demodulation.demodulate_signal(signal_type,preprocessed_signal)
    np.savetxt('result.dat',demodulated_signal)
    
    # 参数估计
    parameters = parameter_estimation.estimate_parameters(signal_type,demodulated_signal,preprocessed_signal)

    # 显示结果
    user_interface.display_signal_info(signal_type, parameters)
    result=np.loadtxt('result.dat')
    result=result-result.mean()
    np.savetxt('result.dat',result)
    
    # 输出解调信号供示波器观测
    signal_IO.signal_output(result)

    # 采样信号、解调信号绘图
    plt.plot(signal_sample)
    plt.savefig('data.png')
    plt.clf()
    plt.plot(result)
    plt.savefig('result.png')
    
    # 关闭设备
    signal_IO.close_device()
    
    
if __name__ == "__main__":
    main()
