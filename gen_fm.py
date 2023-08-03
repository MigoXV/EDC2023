import numpy as np

# 设置参数
baseband_frequency = 5000  # 基带信号频率
carrier_frequency = 2e6  # 载波频率
amplitude = 50  # 幅度，对应100mVpp
sampling_rate = 8e6  # 采样率
num_samples = 8000  # 生成的样本点数
time = np.arange(num_samples) / sampling_rate  # 时间向量

# 生成基带信号
baseband_signal = np.sin(2 * np.pi * baseband_frequency * time)

# 进行FM调制
mod_index = 1  # 调频指数，可根据需要调整
carrier_signal = np.sin(2 * np.pi * carrier_frequency * time +
                        mod_index * np.cos(2 * np.pi * baseband_frequency * time))

# 调整幅度
carrier_signal = carrier_signal * amplitude

# 保存数据到文件
np.savetxt('data-fm.dat', carrier_signal)

import matplotlib.pyplot as plt

plt.plot(carrier_signal)
plt.show()
