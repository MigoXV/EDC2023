import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Coefficients from your MATLAB IIR filter
NUM = np.array([
    [0.4813925341436, 0, 0],
    [1, -1.999967361529, 1],
    [0.4390710184324, 0, 0],
    [1, -1.999961353389, 1],
    [0.3504860308344, 0, 0],
    [1, -1.999944013261, 1],
    [0.216221663083, 0, 0],
    [1, -1.999890599948, 1],
    [0.06965568499512, 0, 0],
    [1, -1.999597163089, 1],
    [0.002745625195479, 0, 0],
    [1, 1, 0],
    [1, 0, 0]
])

DEN = np.array([
    [1, 0, 0],
    [1, -1.999172123505, 0.9991878354213],
    [1, 0, 0],
    [1, -1.997422718302, 0.9974396869091],
    [1, 0, 0],
    [1, -1.995313036438, 0.9953326590073],
    [1, 0, 0],
    [1, -1.99274850862, 0.9927721632812],
    [1, 0, 0],
    [1, -1.990192987948, 0.9902210478292],
    [1, 0, 0],
    [1, -0.994508749609, 0],
    [1, 0, 0]
])

# normalize coefficients
for i in range(len(NUM)):
    if DEN[i][0] != 0:
        NUM[i] = NUM[i] / DEN[i][0]
        DEN[i] = DEN[i] / DEN[i][0]

# Create your IIR filter by cascading the 2nd order sections
sos = np.stack((NUM[:, 0:3], DEN[:, 0:3]), axis=-1)
sos = np.reshape(sos, (-1, 6))

# Now sos is your filter coefficients in second order sections format
# Let's plot the frequency response
w, h = signal.sosfreqz(sos)
plt.plot(w/np.pi, abs(h))
plt.title('Frequency response of IIR filter')
plt.xlabel('Normalized frequency')
plt.ylabel('Gain')
plt.grid(True)
plt.show()
