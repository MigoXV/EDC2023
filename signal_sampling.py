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


if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")



def sample_signal(hzRate = 4e4,cSamples = 8*1024):
        
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
    
    rgdSamples1 = (c_double*cSamples)()
    # rgdSamples2 = (c_double*cSamples)()
    sts = c_int()

    print("Configure analog in")
    dwf.FDwfAnalogInFrequencySet(hdwf, c_double(hzRate))
    dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(-1), c_double(2))
    dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(cSamples))
    dwf.FDwfAnalogInTriggerSourceSet(hdwf, trigsrcAnalogOut1) 
    dwf.FDwfAnalogInTriggerPositionSet(hdwf, c_double(0.6*cSamples/hzRate)) # trigger position at 20%, 0.5-0.3

    print("Starting acquisition...")
    dwf.FDwfAnalogInConfigure(hdwf, c_int(1), c_int(1))

    while True:
        dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
        if sts.value == DwfStateArmed.value :
            break
        time.sleep(0.1)
    print("   armed")

    while True:
        dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
        if sts.value == DwfStateDone.value :
            break
        time.sleep(0.1)
    print("   done")

    dwf.FDwfAnalogInStatusData(hdwf, c_int(0), rgdSamples1, len(rgdSamples1)) # get channel 1 data

    dwf.FDwfDeviceCloseAll()
    
    return numpy.array(rgdSamples1)
# plt.plot(numpy.linspace(0, cSamples-1, cSamples), numpy.fromiter(rgdSamples1, dtype = numpy.float))
# plt.show()
