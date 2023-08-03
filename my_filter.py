import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

def AM_filter(origin_signal):
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
    # BL = 21
    output_signal=np.convolve(B,origin_signal,'same')
    return output_signal

if __name__=="__main__":
    
    origin_data=np.loadtxt('result.dat')
    result=AM_filter(origin_data)
    plt.subplot(2,1,1)
    plt.plot(origin_data)
    plt.subplot(2,1,2)
    plt.plot(result)
    plt.show()