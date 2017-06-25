import wave
import struct
import numpy
import os
import sys
from shutil import copyfile


hz = 16000
def read_wav(wav_file):
     """Returns two chunks of sound data from wave file."""
     w = wave.open(wav_file)
     frames = w.readframes(w.getnframes())
     wav_data = struct.unpack('%dh' % w.getnframes(), frames)
     return (wav_data)


def moments(x):
    mean = x.mean()
    std = x.var() ** 0.5
    skewness = ((x - mean) ** 3).mean() / std ** 3
    kurtosis = ((x - mean) ** 4).mean() / std ** 4
    return [mean, std, skewness, kurtosis]

def detectfrequency(wavdata):
    w = numpy.fft.fft(wavdata)
    freqs = numpy.fft.fftfreq(len(w))

    # Find the peak in the coefficients
    idx = numpy.argmax(numpy.abs(w))
    freq = freqs[idx]
    freq_in_hertz = abs(freq * hz)
    print(freq_in_hertz)
    return freq_in_hertz



def fftfeatures(wavdata):
    f = numpy.fft.fft(wavdata)
    halfIdx = (int)(f.size / 2 + 1)
    f = f[2:halfIdx]
    f = abs(f)
    total_power = f.sum()
    f = numpy.array_split(f, 10)


    return [e.sum() / total_power for e in f]


def features(x):
    x = numpy.array(x)
    f = []

    xs = x
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    xs = x.reshape(-1, 10).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    xs = x.reshape(-1, 100).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    xs = x.reshape(-1, 1000).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    f.extend(fftfeatures(x))
    return f

sexDict={'f':'0', 'm':'1'}
retDict={'hu':'1', 'bu':'2', 'bp':'3', 'dc':'4', 'ti':'5', 'lo':'6', 'ch':'7', 'sc':'8', 'dk':'9'}
# inputDir='C:\\Data\\Document\\Hackathon\\audio\\input'
# outputDir='C:\\Data\\Document\\Hackathon\\audio\\output'
# dataType={'training':'training set.csv', 'test':'test set.csv'}

# inputDir='C:\\Data\\Document\\Hackathon\\audio\\record'
# outputDir='C:\\Data\\Document\\Hackathon\\audio\\record'
# dataType={'input':'training set.csv', 'output':'test set.csv'}

if len(sys.argv) < 3:
    print('Error!!! please pass input folder and output file path.')
    sys.exit(1)

inputDir=sys.argv[1]
outputFile=sys.argv[2]

def exportFile(fileName, hrz, data, maxLen):
    with open(outputFile, 'a') as test_file:
        (fname, ext) = os.path.splitext(fileName)
        infoArr = fname.split('-')
        regularName = True
        if len(infoArr) < 9:
            sex = '0';age = '0';ret = '0'
            regularName = False
        else:
            sex = infoArr[7];age = infoArr[8];ret = infoArr[9]
        # sex = infoArr[7];age = infoArr[8];ret = infoArr[9]
        dtStr = ','.join([str(s) for s in list(data)])
        dtStr = dtStr + ',0' * (maxLen - len(data))
        # for num in data:
        #     test_file.write('{},'.format(num))
        # lineStr = retDict[str(ret)] + ',' + str(sexDict[sex]) + ',' + str(age) + ',' + str(int(round(hrz))) + ',' + dtStr + '\n'
        if regularName:
            lineStr = str(sexDict[sex]) + ',' + str(age) + ',' + str(int(round(hrz))) + ',' + dtStr + '\n'
        else:
            lineStr = sex + ',' + age + ',' + str(int(round(hrz))) + ',' + dtStr + '\n'
        test_file.write(lineStr)

fidx = 0
isNewOutputFile=False
if os.path.isfile(inputDir):
    if not inputDir.endswith('.wav'):
        sys.exit(0)
    try:
        data = read_wav(inputDir)
        volume = abs(sum(data) / len(data))
        print(volume)
        hrz = detectfrequency(data)
        if os.path.exists(outputFile):
            os.remove(outputFile)
            fobj = open(outputFile, 'w')
            fobj.close();

        exportFile(os.path.split(inputDir)[1], hrz, data, 0)
    except:
        print(sys.exc_info()[0])
        sys.exit(1)
else:
    for path, dirs, files in os.walk(inputDir):
        maxLen = 0;
        for tempf in files:
            if not tempf.endswith('.wav'):
                continue
            tempWav_file = os.path.join(path, tempf)
            tempdt = read_wav(tempWav_file)
            if len(tempdt) > maxLen:
                maxLen = len(tempdt)

        for f in files:
            if not f.endswith('.wav'):
                continue
            wav_file = os.path.join(path, f)
            tail, track = os.path.split(wav_file)
            tail, dir1 = os.path.split(tail)
            tail, dir2 = os.path.split(tail)
            try:
                print(wav_file)
                data = read_wav(wav_file)
                volume = abs(sum(data)/len(data))
                print(volume)
                hrz = detectfrequency(data)
                if isNewOutputFile == False:
                    if os.path.exists(outputFile):
                        os.remove(outputFile)
                        fobj = open(outputFile,'w')
                        fobj.close();
                        isNewOutputFile = True

                exportFile(f, hrz, data, maxLen)
                # if hrz > 400 and volume > 0.1:
                #     copyfile(wav_file, "C:\\Data\\Document\\Hackathon\\audio\\result\\3GP\\Collection\\"+track)
            except:
                print(sys.exc_info()[0])
                continue