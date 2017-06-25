import numpy as np
from PreFlight import const
from sklearn import preprocessing
from PreFlight import const as cnst

def getFeatures(onelineArray):
    startIdx = 0
    endIdx = startIdx + 399
    rs = []
    while endIdx < len(onelineArray):
        tmp = onelineArray[startIdx:endIdx]
        startIdx = endIdx + 1
        endIdx = startIdx + 399
        mean = tmp.mean()
        std = tmp.var() ** 0.5
        rs.append([mean,std])
    return rs

def loadCNNTrain():
    data_train_x = np.array([])
    data_train_y = np.array([])
    with open(const.param_data_cnn) as f:
        for line in f:
            array = np.fromstring(line,dtype=float,sep=",")
            tmp_y = [0] * 9
            idx = (int)(array[0] - 1)
            tmp_y[idx] = 1
            fe = getFeatures(array[4:112004])

            data_train_x = np.insert(data_train_x, 0, fe)
            data_train_y = np.insert(data_train_y, 0, tmp_y)

    data_train_x = data_train_x.reshape(-1,cnst.CNN_FEATURE,2)
    data_train_y = data_train_y.reshape(-1,9)
    return [data_train_x,data_train_y]

def loadCNNTest():
    data_test_x = np.array([])
    data_test_y = np.array([])
    with open(const.param_data_cnn) as f:
        for line in f:
            array = np.fromstring(line, dtype=float, sep=",")
            tmp_y = [0] * 9
            idx = (int)(array[0] - 1)
            tmp_y[idx] = 1
            fe = getFeatures(array[4:112004])
            data_test_x = np.insert(data_test_x, 0, fe)
            data_test_y = np.insert(data_test_y, 0, tmp_y)

    data_test_x = data_test_x.reshape(-1, cnst.CNN_FEATURE)
    data_test_y = data_test_y.reshape(-1, 9)
    #data_test_x = preprocessing.scale(data_test_x)

    return [data_test_x, data_test_y]

def getFinalImage(oimg):
    startIdx = 0
    rs = np.array([])
    for oneSecondData in oimg:
        while startIdx < 10:
            tmp = oneSecondData[startIdx:startIdx+1600]
            startIdx += 1
            mean = tmp.mean()
            #std = tmp.var() ** 0.5
            rs.extend(mean)
    rs.reshape(-1,10)
