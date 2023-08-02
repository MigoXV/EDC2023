import numpy as np
import matplotlib.pyplot as plt
# from scipy.signal import hilbert
import signal_demodulation

point=8192
n=np.array(range(point))
v0=0.1/2
v_omega=0.01
# ka=8
# ma=ka*v_omega/v0
ma=0.5
ka=ma*v0/v_omega
print(f'ka={ka:.2f}')
fs=10e6
fa=10e3
fcarrier=2e6
V_omega=0.01

T=fs/fa
print("T=",T)
omega0=2*np.pi/T
print("omega0=","{:.5f}".format(omega0))

modulating_wave=v_omega*np.sin(omega0*n)
plt.subplot(2,2,1)
plt.plot(modulating_wave)
plt.title('modulating_wave')
# plt.show()

Tc=fs/fcarrier
print("Tc=",Tc)
omegac=2*np.pi/Tc
print("omegac=","{:.5f}".format(omegac))

carrier=v0*np.sin(omegac*n)
plt.subplot(2,2,2)
plt.plot(carrier)
plt.title('carrier')
# plt.show()


modulated_wave=(v0+ka*modulating_wave)*carrier
plt.subplot(2,2,3)
plt.plot(modulated_wave)
# plt.show()

result=signal_demodulation.demodulate_signal('AM',modulated_wave)
plt.subplot(2,2,4)
plt.plot(result)

plt.show()
