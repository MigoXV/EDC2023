import matplotlib.pyplot as plt
import numpy as np

data=np.loadtxt('data.dat')
plt.plot(data)
plt.show()
plt.savefig('test_plot.png')