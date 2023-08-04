import matplotlib.pyplot as plt
import numpy as np

data=np.loadtxt('result.dat')
plt.plot(data)
plt.show()
plt.savefig('test_plot.png')