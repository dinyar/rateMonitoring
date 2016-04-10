#!/bin/python
import glob
from datetime import datetime
import pytz
from matplotlib import pyplot as plt
from matplotlib.dates import date2num
import argparse

desc = "Tool to extract rates from tdf dumps"

parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('filename', type=str, default='rates_', help='Generic part of TDF dump filename (i.e. part excluding timestamp).')
parser.add_argument('path', type=str, default='', help='Path to folder with TDF dumps.')
opts = parser.parse_args()

#algos = ['|   41 |', '|   33 |', '|  165 |', '|  152 |']
algos = ['|   41 |', '|   33 |', '|  165 |']

dateList = []
rateList = [[] for x in xrange(0,len(algos))]
if opts.path == '':
    path = ''
elif opts.path[-1] != '/':
    path = opts.path + '/'
else:
    path = opts.path
for filename in glob.glob(path + opts.filename + '*'):
    datetimeString = filename[filename.find(opts.filename)+len(opts.filename):]
    year = int(datetimeString[0:4])
    month = int(datetimeString[4:6])
    day = int(datetimeString[6:8])
    hour = int(datetimeString[9:11])
    minute = int(datetimeString[11:13])
    date = datetime(year, month, day, hour, minute)
    dateList.append(date)
    with open(filename) as f:
        index = 0
        for line in f:
            for algo in algos:
                if algo in line:
                    startPos = line.find(algo)+len(algo)
                    rate = int(line[startPos:line.find('|', startPos)])
                    rateList[index].append(rate)
                    index += 1

x = [date2num(date) for date in dateList]

fig = plt.figure()
graph = fig.add_subplot(111)
#graph.plot(x, rateList[1], 'ro', x, rateList[0], 'bs', x, rateList[2], 'y*', x, rateList[3], 'g^')
graph.plot(x, rateList[1], 'ro', x, rateList[0], 'bs', x, rateList[2], 'g^')
graph.set_xticks(x)

#legend = graph.legend(['SingleEG5', 'SingleMuOpen', 'SingleJet8', 'BPTX AND'], numpoints=1)
legend = graph.legend(['SingleEG5', 'SingleMuOpen', 'BPTX AND'], numpoints=1)

graph.set_xticklabels(
    [date.strftime("%Y-%m-%d-%H:%M") for date in dateList]
    )
fig.autofmt_xdate()
plt.ylabel('Rate [Hz]')
plt.show()


