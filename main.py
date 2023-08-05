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
import params_average
import params_median

def main():
    parameter_average={}
    with open('parameter.json','w',encoding='UTF-8') as f:
        f.write(json.dumps(parameter_average))
    # while True:
        
    # 初始化设备
    signal_IO.initialize_device()
    
    times=0
    
    average_times=20
    
    
    while True:
        # 一键启动
        print('---------按enter键开始第',times+1,'次测量---------------')
        key=input()
        if key=='quit':
            break
        
        parameters=[{}]*average_times
        signal_type=['']*average_times

        for count in range(average_times):
        
            # 采样信号
            signal_sample=signal_IO.signal_sampling()

            # 预处理信号
            # preprocessed_signal = signal_preprocessing.preprocess_signal(signal_sample)
            preprocessed_signal=signal_sample
            
            # 识别信号类型
            signal_type[count] = signal_identification.identify_signal(preprocessed_signal)

        parameter_type=params_median.paramater_type(signal_type,average_times)
        signal_type=[parameter_type]*20

        for count in range(average_times):

            # 解调信号
            demodulated_signal = signal_demodulation.demodulate_signal(signal_type[count],preprocessed_signal)
            np.savetxt('result.dat',demodulated_signal)
        
        for count in range(average_times):
        
            # 参数估计
            parameters[count] = parameter_estimation.estimate_parameters(signal_type[count],demodulated_signal,preprocessed_signal)
        
        # parameter_average['type']=parameter_type
        parameter_average=params_median.parameter_median(parameter_type,parameters,average_times)
        
        # 显示结果
        user_interface.display_signal_info(parameter_type, parameter_average)
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
        
        times+=1
             
        print()
    
    # 关闭设备
    signal_IO.close_device()
    
    
if __name__ == "__main__":
    main()
