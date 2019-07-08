import numpy as np

def timebin(arr,t):
    counter =0
    binnedArray = [0]

    i = 0
    while i < (len(arr)):
        if arr[i]>=counter*t:
            counter += 1
            binnedArray.append(0)
            continue
        i+=1
        binnedArray[-1]+=1
    
    return list(np.array(binnedArray))

def pad(arr1, arr2):
    if len(arr1)> len(arr2):
        for i in range(len(arr1)-len(arr2)):
            arr2.append(0)
    else:
        for i in range(len(arr2)-len(arr1)):
            arr1.append(0)
            
    return [arr1, arr2]