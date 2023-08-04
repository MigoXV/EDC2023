import numpy as np

def get_max_subarray(arr):
    # 找到第一个最大值和对应的索引
    max_1_idx = np.argmax(arr)
    max_1_value = arr[max_1_idx]

    # 检查索引+1000是否超出数组范围
    if max_1_idx + 1000 >= len(arr):
        print("The array is not long enough after the first max value")
        return None

    # 在索引+1000后的数据中找到第一个最大值并记录其索引
    sub_arr = arr[max_1_idx + 1000:]
    max_2_idx = np.argmax(sub_arr) + max_1_idx + 1000

    # 截取两索引之间的数据
    result_arr = arr[max_1_idx:max_2_idx]

    return result_arr
