"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2018-07-19

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
import time
from dwfconstants import *
import sys
import matplotlib.pyplot as plt
import numpy as np
import json
import output_con_phase


if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

with open('config.json') as f:
    result=json.loads(f.read())

cSamples=result['nSamples']
hzFreq=result['fs']

# continue running after device close, prevent temperature drifts
dwf.FDwfParamSet(c_int(4), c_int(0)) # 4 = DwfParamOnClose, 0 = continue 1 = stop 2 = shutdown

#print(DWF version
# version = create_string_buffer(16)
# dwf.FDwfGetVersion(version)
# print("DWF Version: "+str(version.value))

#open device
hdwf = c_int()
print("===========================================================================")
print("Opening first device for output")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == hdwfNone.value:
    print("failed to open device")
    quit()


# hzFreq = 8e6
# cSamples = 8192
# hdwf = c_int()
rgdSamples = (c_double*cSamples)()
channel = c_int(0)

# 从数据文件中读取数据，并保存到列表中
# with open('result.dat', 'r') as file:
#     data = file.readlines()
data=np.loadtxt('result.dat')

con_phase_data=output_con_phase.get_max_subarray(data)
cSamples=len(con_phase_data)

plt.plot(con_phase_data)
plt.savefig('con_phase_data.png')

# 将数据转换为double类型，并保存到ctypes数组中
for i in range(cSamples):
    rgdSamples[i] = c_double(float(con_phase_data[i]))

# dwf.FDwfAnalogOutNodeEnableSet(hdwf, channel, AnalogOutNodeCarrier, c_bool(True))
# dwf.FDwfAnalogOutNodeFunctionSet(hdwf, channel, AnalogOutNodeCarrier, funcSine)
# dwf.FDwfAnalogOutNodeFrequencySet(hdwf, channel, AnalogOutNodeCarrier, c_double(2e6))
# dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, channel, AnalogOutNodeCarrier, c_double(0.1))
# dwf.FDwfAnalogOutNodeOffsetSet(hdwf, channel, AnalogOutNodeCarrier, c_double(0))

print("Generating custom waveform from file result.dat")
dwf.FDwfAnalogOutNodeEnableSet(hdwf, channel, AnalogOutNodeCarrier, c_bool(True))
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, channel, AnalogOutNodeCarrier, funcCustom) 
dwf.FDwfAnalogOutNodeDataSet(hdwf, channel, AnalogOutNodeCarrier, rgdSamples, c_int(cSamples))
dwf.FDwfAnalogOutNodeFrequencySet(hdwf, channel, AnalogOutNodeCarrier, c_double(hzFreq/cSamples)) 
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, channel, AnalogOutNodeCarrier, c_double(2.0))
dwf.FDwfAnalogOutConfigure(hdwf, channel, c_int(1))

dwf.FDwfDeviceCloseAll()
print("===========================================================================")
