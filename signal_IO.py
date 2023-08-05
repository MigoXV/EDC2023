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

with open('config.json') as f:
    result=json.loads(f.read())

nSamples=result['nSamples']
fs=result['fs']

dwf.FDwfParamSet(c_int(4), c_int(0))

#declare ctype variables
hdwf = c_int()
sts = c_byte()
rgdSamples_input = (c_double*nSamples)()
rgdSamples_output = (c_double*nSamples)()
# version = create_string_buffer(16)
# dwf.FDwfGetVersion(version)
# print("DWF Version: "+str(version.value))

# 彩色显示：print('\033[显示方式；前景色；背景色m  需要显示的文字  \033[0m')
# eg:       print('\033[0;36m abc \033[0m')
#open device

# dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))
# print("===========================================================================")
# print("\033[0;31mdevice opened \033[0m")


# if hdwf.value == hdwfNone.value:
#     szerr = create_string_buffer(512)
#     dwf.FDwfGetLastErrorMsg(szerr)
#     print(szerr.value)
#     print("033[0;31m failed to open device \033[0m")
#     quit()

# # cBufMax = c_int()
# # dwf.FDwfAnalogInBufferSizeInfo(hdwf, 0, byref(cBufMax))
# # print("Device buffer size: "+str(cBufMax.value)) 

# #set up acquisition
# dwf.FDwfAnalogInFrequencySet(hdwf, c_double(fs))
# dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(nSamples)) 
# dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(-1), c_bool(True))
# dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(-1), c_double(5))
# dwf.FDwfAnalogInChannelFilterSet(hdwf, c_int(-1), filterDecimate)

# #wait at least 2 seconds for the offset to stabilize
# time.sleep(2)

def initialize_device():
    global hdwf
    dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))
    print("===========================================================================")
    print("\033[0;31mdevice opened \033[0m")


    if hdwf.value == hdwfNone.value:
        szerr = create_string_buffer(512)
        dwf.FDwfGetLastErrorMsg(szerr)
        print(szerr.value)
        print("033[0;31m failed to open device \033[0m")
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
    
    
def signal_sampling():

    global sts,hdwf
    rgdSamples_input = (c_double*nSamples)()


    print("Starting oscilloscope")
    dwf.FDwfAnalogInConfigure(hdwf, c_int(1), c_int(1))


    while True:
        dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
        if sts.value == DwfStateDone.value :
            break
        time.sleep(0.1)
    print("Acquisition done")

    dwf.FDwfAnalogInStatusData(hdwf, 0, rgdSamples_input, nSamples) # get channel 1 data
    #dwf.FDwfAnalogInStatusData(hdwf, 1, rgdSamples, 4000) # get channel 2 data
    # dwf.FDwfDeviceCloseAll()

    # #plot window
    # dc = sum(rgdSamples)/len(rgdSamples)
    # print("DC: "+str(dc)+"V")
    rgdSamples_input=numpy.array(rgdSamples_input)
    
    return rgdSamples_input

def signal_output(data):
    
    with open('parameter.json') as f:
        params=json.loads(f.read())
        
    if params['type']=='AM' or params['type']=='FM':
        output_wave_form=funcSine
        output_wave_amplitude=params['ma']*2
    else:
        output_wave_form=funcSquare
        
    output_wave_frequency=params['T_num']*1000
    
    channel = c_int(0)
    
    global rgdSamples_output
    
    for i in range(nSamples):
        rgdSamples_output[i] = c_double(float(data[i]))
        
    print("Generating custom waveform from file result.dat")
    dwf.FDwfAnalogOutNodeEnableSet(hdwf, channel, AnalogOutNodeCarrier, c_bool(True))
    dwf.FDwfAnalogOutNodeFunctionSet(hdwf, channel, AnalogOutNodeCarrier, output_wave_form) 
    dwf.FDwfAnalogOutNodeDataSet(hdwf, channel, AnalogOutNodeCarrier, rgdSamples_output, c_int(nSamples))
    dwf.FDwfAnalogOutNodeFrequencySet(hdwf, channel, AnalogOutNodeCarrier, c_double(output_wave_frequency)) 
    dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, channel, AnalogOutNodeCarrier, c_double(output_wave_amplitude))
    dwf.FDwfAnalogOutConfigure(hdwf, channel, c_int(1))
    

def close_device():
    dwf.FDwfDeviceCloseAll()
 

def test():
    
    global sts,rgdSamples_input,hdwf
    
    
    # #set up acquisition
    # dwf.FDwfAnalogInFrequencySet(hdwf, c_double(fs))
    # dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(nSamples)) 
    # dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(-1), c_bool(True))
    # dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(-1), c_double(5))
    # dwf.FDwfAnalogInChannelFilterSet(hdwf, c_int(-1), filterDecimate)

    # #wait at least 2 seconds for the offset to stabilize
    # time.sleep(2)

    # print("Starting oscilloscope")
    # dwf.FDwfAnalogInConfigure(hdwf, c_int(1), c_int(1))


    # while True:
    #     dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
    #     if sts.value == DwfStateDone.value :
    #         break
    #     time.sleep(0.1)
    # print("Acquisition done")

    # dwf.FDwfAnalogInStatusData(hdwf, 0, rgdSamples_input, nSamples) # get channel 1 data
    # # dwf.FDwfDeviceCloseAll()
    data=numpy.loadtxt('data.dat')
    for i in range(nSamples):
        rgdSamples_output[i] = c_double(float(data[i]))
    # =========================输出部分===========================================
    channel = c_int(0)
    print("Generating custom waveform from file result.dat")
    dwf.FDwfAnalogOutNodeEnableSet(hdwf, channel, AnalogOutNodeCarrier, c_bool(True))
    dwf.FDwfAnalogOutNodeFunctionSet(hdwf, channel, AnalogOutNodeCarrier, funcSine) 
    dwf.FDwfAnalogOutNodeDataSet(hdwf, channel, AnalogOutNodeCarrier, rgdSamples_input, c_int(nSamples))
    dwf.FDwfAnalogOutNodeFrequencySet(hdwf, channel, AnalogOutNodeCarrier, c_double(fs/nSamples)) 
    dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, channel, AnalogOutNodeCarrier, c_double(2.0))
    dwf.FDwfAnalogOutConfigure(hdwf, channel, c_int(1))
    
    dwf.FDwfDeviceCloseAll()

# if __name__=='__main__':
#     test()

if __name__=='__main__':
    in_data=signal_sampling()
    # in_data=numpy.loadtxt('data.dat')
    # plt.plot(in_data)
    # plt.show()
    signal_output(in_data)

    print("data has been loaded into file data.dat")
    print("===========================================================================")