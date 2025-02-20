"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2018-07-19

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
from dwfconstants import *
import math
import time
import matplotlib.pyplot as plt
import sys
import numpy
import json

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

# with open('config.json') as f:
#     result=json.loads(f.read())

nSamples=8000
fs=80e6
#declare ctype variables
hdwf = c_int()
sts = c_byte()
rgdSamples = (c_double*nSamples)()

# version = create_string_buffer(16)
# dwf.FDwfGetVersion(version)
# print("DWF Version: "+str(version.value))

#open device
print("===========================================================================")
print("Opening first device for input")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == hdwfNone.value:
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(szerr.value)
    print("failed to open device")
    quit()

# cBufMax = c_int()
# dwf.FDwfAnalogInBufferSizeInfo(hdwf, 0, byref(cBufMax))
# print("Device buffer size: "+str(cBufMax.value)) 

#set up acquisition
dwf.FDwfAnalogInFrequencySet(hdwf, c_double(fs))
dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(nSamples)) 
dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(-1), c_bool(True))
dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(-1), c_double(5))
dwf.FDwfAnalogInChannelFilterSet(hdwf, c_int(-1), filterDecimate)

#wait at least 2 seconds for the offset to stabilize
time.sleep(2)

print("Starting oscilloscope")
dwf.FDwfAnalogInConfigure(hdwf, c_int(1), c_int(1))


while True:
    dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
    if sts.value == DwfStateDone.value :
        break
    time.sleep(0.1)
print("Acquisition done")

dwf.FDwfAnalogInStatusData(hdwf, 0, rgdSamples, nSamples) # get channel 1 data
#dwf.FDwfAnalogInStatusData(hdwf, 1, rgdSamples, 4000) # get channel 2 data
dwf.FDwfDeviceCloseAll()

# #plot window
# dc = sum(rgdSamples)/len(rgdSamples)
# print("DC: "+str(dc)+"V")
rgdSamples=numpy.array(rgdSamples)


numpy.savetxt('data_is_cw.dat',rgdSamples)

data=numpy.loadtxt('data_is_cw.dat')
# plt.plot(data)
# plt.show()

print("data has been loaded into file data.dat")
print("===========================================================================")