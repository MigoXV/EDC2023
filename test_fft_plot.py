import matplotlib.pyplot as plt
import numpy as np

import signal_sampling
data=np.loadtxt('data.dat')
fft_data=np.fft.fft(data)
fft_data_abs=abs(fft_data)
plt.plot(fft_data_abs,'o')
plt.show()
plt.savefig('test_fft_plot.png')