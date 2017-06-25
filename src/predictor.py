import numpy
import sys
import math
from sklearn import preprocessing

def moments(x):
    mean = x.mean()
    std = x.var() ** 0.5
    skewness = ((x - mean) ** 3).mean() / std ** 3
    kurtosis = ((x - mean) ** 4).mean() / std ** 4
    return [mean, std, skewness, kurtosis]

def fftfeatures(wavdata):
    f = numpy.fft.fft(wavdata)
    halfIdx = (int)(f.size / 2 + 1)
    f = f[2:halfIdx]
    f = abs(f)
    total_power = f.sum()
    f = numpy.array_split(f, 10)
    return [e.sum() / total_power for e in f]

def features(x):
    alignment = math.floor(len(x) / 16000)
    til = (16000 * alignment)


    x = numpy.array(x[0:til])
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

    xs = x.reshape(-1, 320).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    f.extend(fftfeatures(x))

    return f


def loadPredict(file):
    data_x = numpy.array([])
    with open(file) as f:
        for line in f:
            array = numpy.fromstring(line,dtype=float,sep=",")
            tmp_f = array[0:2]
            tmp_x = array[3:]
            tmp_f = numpy.concatenate((tmp_f, features(tmp_x)))
            data_x = numpy.insert(data_x,0,tmp_f)

    data_x = data_x.reshape(-1,1)
    data_x = preprocessing.scale(data_x)

    return [data_x,[]]

weights = numpy.genfromtxt("Weights.csv",delimiter=',')
bias = numpy.genfromtxt("bias.csv",delimiter=',')

weights = numpy.asmatrix(weights)
bias = numpy.asmatrix(bias).T

if len(sys.argv) < 3:
    print("Please specify the input and output file")
else:
    data_file = sys.argv[1]
    out_file = sys.argv[2]
    [predict, empty] = loadPredict(data_file)
    predict = numpy.asmatrix(predict)

    rs = weights.T * predict + bias
    rs = [abs(number) for number in rs]
    total = sum(rs)
    rs = [(number / total) for number in rs]
    final = max(rs)
    category = [i for i, j in enumerate(rs) if j == final][0]
    categoryLabel = ['hungry','needs burping','belly pain','discomfort','tired','lonely','cold / hot','scared','don\'t know']

    print(categoryLabel[category])

    text_file = open(out_file, "w")
    text_file.write(categoryLabel[category])
    text_file.write("\n")
    for item in rs:
        text_file.write("%s\n" % item)
    text_file.close()
