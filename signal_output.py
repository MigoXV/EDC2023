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
import numpy
import json

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

with open('config,json') as f:
    result=json.loads(f.read())

nSamples=result['nSamples']
fs=result['fs']

# continue running after device close, prevent temperature drifts
dwf.FDwfParamSet(c_int(4), c_int(0)) # 4 = DwfParamOnClose, 0 = continue 1 = stop 2 = shutdown

#print(DWF version
version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

#open device
hdwf = c_int()
print("Opening first device...")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == hdwfNone.value:
    print("failed to open device")
    quit()


hzMid = 10e3
secSweep = 5e-3
channel = c_int(0)

dwf.FDwfAnalogOutNodeEnableSet(hdwf, channel, AnalogOutNodeCarrier, c_bool(True))
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, channel, AnalogOutNodeCarrier, funcSine)
dwf.FDwfAnalogOutNodeFrequencySet(hdwf, channel, AnalogOutNodeCarrier, c_double(2e6))
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, channel, AnalogOutNodeCarrier, c_double(0.1))
dwf.FDwfAnalogOutNodeOffsetSet(hdwf, channel, AnalogOutNodeCarrier, c_double(0))

dwf.FDwfAnalogOutNodeEnableSet(hdwf, channel, AnalogOutNodeAM, c_bool(True))
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, channel, AnalogOutNodeAM, funcSine)
dwf.FDwfAnalogOutNodeFrequencySet(hdwf, channel, AnalogOutNodeAM, c_double(10e3))
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, channel, AnalogOutNodeAM, c_double(40))
dwf.FDwfAnalogOutNodeSymmetrySet(hdwf, channel, AnalogOutNodeAM, c_double(50))

# dwf.FDwfAnalogOutRunSet(hdwf, channel, c_double(secSweep*100))
# dwf.FDwfAnalogOutRepeatSet(hdwf, channel, c_int(100))
dwf.FDwfAnalogOutConfigure(hdwf, channel, c_int(1))

dwf.FDwfDeviceCloseAll()

