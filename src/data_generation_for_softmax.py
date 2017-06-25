import numpy as np
from PreFlight import const
from PreFlight import data_generation_for_softmax as gd
import math
from sklearn import preprocessing

def iterate_minibatches(inputs, targets, batchsize, shuffle=False):
    assert inputs.shape[0] == targets.shape[0]
    if shuffle:
        indices = np.arange(inputs.shape[0])
        np.random.shuffle(indices)
    for start_idx in range(0, inputs.shape[0] - batchsize + 1, batchsize):
        if shuffle:
            excerpt = indices[start_idx:start_idx + batchsize]
        else:
            excerpt = slice(start_idx, start_idx + batchsize)
        yield inputs[excerpt], targets[excerpt]

def loadTrain():
    data_train_x = np.array([])
    data_train_y = np.array([])
    with open(const.param_data_source) as f:
        for line in f:
            array = np.fromstring(line,dtype=float,sep=",")
            tmp_y = [0] * 9
            idx = (int)(array[0] - 1)
            tmp_y[idx] = 1
            tmp_f = array[1:3]
            tmp_x = array[4:]
            tmp_f = np.concatenate((tmp_f, gd.features(tmp_x)))
            data_train_y = np.insert(data_train_y,0,tmp_y)
            data_train_x = np.insert(data_train_x,0,tmp_f)

    data_train_x = data_train_x.reshape(-1,const.param_feature_num)
    data_train_y = data_train_y.reshape(-1,const.param_final_category)
    data_train_x = preprocessing.scale(data_train_x)
    #tsne = TSNE(perplexity=30, n_components=8, init='pca', n_iter=5000)
    #data_train_x = tsne.fit_transform(data_train_x)
    return [data_train_x,data_train_y]

def loadTest():
    data_test_x = np.array([])
    data_test_y = np.array([])
    with open(const.param_data_source) as f:
        for line in f:
            array = np.fromstring(line,dtype=float,sep=",")
            tmp_y = [0] * 9
            idx = (int)(array[0] - 1)
            tmp_y[idx] = 1
            tmp_f = array[1:3]
            tmp_x = array[4:]
            tmp_f = np.concatenate((tmp_f, gd.features(tmp_x)))
            data_test_y = np.insert(data_test_y,0,tmp_y)
            data_test_x = np.insert(data_test_x,0,tmp_f)

    data_test_x = data_test_x.reshape(-1,const.param_feature_num)
    data_test_y = data_test_y.reshape(-1,const.param_final_category)
    #tsne = TSNE(perplexity=30, n_components=8, init='pca', n_iter=5000)
    #data_test_x = tsne.fit_transform(data_test_x)
    data_test_x = preprocessing.scale(data_test_x)
    return [data_test_x,data_test_y]

def moments(x):
    mean = x.mean()
    std = x.var() ** 0.5
    skewness = ((x - mean) ** 3).mean() / std ** 3
    kurtosis = ((x - mean) ** 4).mean() / std ** 4
    return [mean, std, skewness, kurtosis]

def fftfeatures(wavdata):
    f = np.fft.fft(wavdata)
    halfIdx = (int)(f.size / 2 + 1)
    f = f[2:halfIdx]
    f = abs(f)
    total_power = f.sum()
    f = np.array_split(f, 10)
    return [e.sum() / total_power for e in f]

def features(x):
    alignment = math.floor(len(x) / 16000)
    til = (16000 * alignment)

    x = np.array(x[0:til])
    f = []

    xs = x
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    xs = x.reshape(-1, 16).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    xs = x.reshape(-1, 160).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    xs = x.reshape(-1, 800).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    f.extend(fftfeatures(x))

    return f

def loadPredict(file):
    data_x = np.array([])
    with open(file) as f:
        for line in f:
            array = np.fromstring(line,dtype=float,sep=",")
            tmp_f = array[0:2]
            tmp_x = array[3:]
            tmp_f = np.concatenate((tmp_f, gd.features(tmp_x)))
            data_x = np.insert(data_x,0,tmp_f)

    data_x = data_x.reshape(-1,1)
    data_x = preprocessing.scale(data_x)
    #tsne = TSNE(perplexity=30, n_components=8, init='pca', n_iter=5000)
    #data_train_x = tsne.fit_transform(data_train_x)
    return [data_x,[]]
"""file_data = loadData("C:\\Project\\2017Hackthon\\test-small.csv")
y = file_data[:,0]
x = file_data[:,2:]
f = features(x)
print(f)"""