import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
import json

with open('config.json') as f:
    config=json.loads(f.read())

fs=config['fs']
nSamples=config['nSamples']



def test_filter(filename,filter_func):
    def warpfunc():
        origin_data=np.loadtxt(filename)
        result=filter_func(origin_data)
        plt.subplot(2,1,1)
        plt.plot(origin_data)
        plt.subplot(2,1,2)
        plt.plot(result)
        plt.show()
    
    warpfunc()
        

def AM_filter_before(origin_signal):
    a=1
    numtaps=51
    B=scipy.signal.firwin(numtaps,[1.8e6/fs,2.2e6/fs],pass_zero=False)
    plt.plot(abs(np.fft.fft(B)))
    plt.show()
    output_signal=np.convolve(B,origin_signal,'same')
    return output_signal    

def AM_filter_after(origin_signal):
    B = np.array(
        [
            0, 0.004259777142907,  0.01205719520257,  0.02286394914624,
            0.0358571455732,  0.04999985382271,  0.06414261019735,  0.07713593889869,
            0.08794287473966,   0.0957404724666,   0.1000003656201,   0.0957404724666,
            0.08794287473966,  0.07713593889869,  0.06414261019735,  0.04999985382271,
            0.0358571455732,  0.02286394914624,  0.01205719520257, 0.004259777142907,
            0
        ]
        )
    a=origin_signal
    # BL = 21
    output_signal=np.convolve(B,origin_signal,'same')
    return output_signal

def FM_filter_after(origin_signal):
    a=1
    numtaps=91
    B=scipy.signal.firwin(numtaps,[0.95e3/fs,5.05e3/fs],pass_zero=False)
    # plt.plot(abs(np.fft.fft(B)))
    # plt.show()
    output_signal=np.convolve(B,origin_signal,'same')
    return output_signal        

# 1.97M-2.03M
def pre_filter(origin_signal):
    a=1
    numtaps=3
    B=scipy.signal.firwin(numtaps,[1.9e6/fs,2.1e6/fs],pass_zero=False)
    # plt.plot(abs(np.fft.fft(B)))
    # plt.show()
    output_signal=np.convolve(B,origin_signal,'same')
    return output_signal      

def phase_filter(origin_signal):
    a=1
    numtaps=50
    B=scipy.signal.firwin(numtaps,[1/fs,50e3/fs],pass_zero=False)
    # plt.plot(abs(np.fft.fft(B)))
    # plt.show()
    output_signal=np.convolve(B,origin_signal,'same')
    return output_signal        
 
def cw_filter(origin_signal):
    a=1
    numtaps=50
    B=scipy.signal.firwin(numtaps,[1.9e6/fs,2.1e6/fs],pass_zero=False)
    # plt.plot(abs(np.fft.fft(B)))
    # plt.show()
    output_signal=np.convolve(B,origin_signal,'same')
    return output_signal    

if __name__=="__main__":
    test_filter('data.dat',AM_filter_before)
        
