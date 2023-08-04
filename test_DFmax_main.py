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
import os

def main():
    params={}
    with open('parameter.json','w',encoding='UTF-8') as f:
        f.write(json.dumps(params))
    with open('DFmax-test-cache.dat','w',encoding='UTF-8') as f:
        pass
    count=0
    FDmax=[0]*25
    while True:
        # 采样信号
        def getdata():
            os.system('python3 /home/jetson/Desktop/EDC2023-bak/EDC2023/signal_sampling.py') #不采样调试时注释本行
            
        getdata()
        signal_sample = np.loadtxt("data.dat")

        # 预处理信号
        # preprocessed_signal = signal_preprocessing.preprocess_signal(signal_sample)
        preprocessed_signal=signal_sample
        # 识别信号类型
        # signal_type = signal_identification.identify_signal(preprocessed_signal)

        # print("信号类型为：",signal_type)

        # if signal_type=='CW':
        #     demodulated_signal=preprocessed_signal
        #     np.savetxt('result.dat',demodulated_signal)
        #     print('signal type:CW')
        # else:
            # 解调信号
        # demodulated_signal = signal_demodulation.demodulate_signal('FMor2FSK',preprocessed_signal)
        demodulated_signal = signal_demodulation.demodulate_signal('FMor2FSK',preprocessed_signal)
        np.savetxt('result.dat',demodulated_signal)
        
        with open('parameter.json','r') as f:
            myjson=json.loads(f.read())
        FDmax[count]=myjson['DFmax']
        # 参数估计
        # parameters = parameter_estimation.estimate_parameters('FMor2FSK',demodulated_signal,preprocessed_signal)

            # 显示结果
            # user_interface.display_signal_info(signal_type, parameters)

        # 输出解调信号供示波器观测
        # user_interface.output_signal()

        # 采样信号、解调信号绘图
        # plt.figure()
        # plt.plot(signal_sample)
        # plt.savefig('data.png')
        # plt.figure()
        plt.plot(demodulated_signal)
        plt.savefig('./DFmax-cache/result-'+str(count+1)+'k.png')
    
        

        with open('DFmax-test-cache.dat','a',encoding='UTF-8') as f:
            f.write(str(FDmax[count])+'\n')
        print('频偏',count+1,'k输入完成，按任意键继续')
        input()
        count+=1
    
if __name__ == "__main__":
    main()
