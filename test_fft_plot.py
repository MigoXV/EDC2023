import matplotlib.pyplot as plt
import numpy as np

import signal_sampling
data=np.loadtxt('data.dat')
fft_data=np.fft.fft(data)
fft_data_abs=abs(fft_data)
fft_data_abs_normalized=fft_data_abs/np.sum(fft_data_abs)
plt.plot(fft_data_abs_normalized,'o')
plt.ylim([0,0.5])
plt.show()
plt.savefig('test_fft_plot.png')