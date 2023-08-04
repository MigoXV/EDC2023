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
    
    count=0
    FDmax=[]
    while True:
        # 采样信号
        import signal_sampling #不采样调试时注释本行
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
        demodulated_signal = signal_demodulation.fm_demodulation(preprocessed_signal)
        np.savetxt('result.dat',demodulated_signal)
        
        with open('parameter.json','r') as f:
            myjson=json.loads(f.read())
        FDmax[count]=json['FDmax']
        # 参数估计
        # parameters = parameter_estimation.estimate_parameters('FMor2FSK',demodulated_signal,preprocessed_signal)

            # 显示结果
            # user_interface.display_signal_info(signal_type, parameters)

        # 输出解调信号供示波器观测
        # user_interface.output_signal()

        # 采样信号、解调信号绘图
        plt.figure()
        plt.plot(signal_sample)
        plt.savefig('data.png')
        plt.figure()
        plt.plot(demodulated_signal)
        plt.savefig('result.png')
    
        count+=1
        input('频偏',count,'k输入完成，按任意键继续')
        with open('parameter.json','a',encoding='UTF-8') as f:
            f.write(json.dumps(FDmax[count]))
    
if __name__ == "__main__":
    main()
