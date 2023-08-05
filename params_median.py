# 导入必要的库，例如 numpy
import numpy as np
import json
import matplotlib.pyplot as plt
# from scipy.fft import fft,fftfreq
import math
import signal_identification
import my_filter
import json

def get_key_median(params_cache,average_times,key):
    key_cache=[0]*average_times
    for count in range(average_times):
        key_cache[count]=params_cache[count][key]
    key_cache=np.array(key_cache)
    key_average=np.median(key_cache)
    return key_average

def parameter_average(signal_type,params_cache,average_times):
    params={}
    
    params['T_num']=get_key_median(params_cache,average_times,'T_num')

    if signal_type == "AM":
        params['ma']=get_key_median(params_cache,average_times,'ma')
    elif signal_type == "FM" or signal_type == "FMor2FSK":
        params['DFmax']=get_key_median(params_cache,average_times,'DFmax')
    else:
        pass
    
    return params


