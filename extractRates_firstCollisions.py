#!/bin/python
import glob
from datetime import datetime
import pytz
from matplotlib import pyplot as plt
from matplotlib.dates import date2num
import argparse

#algos = ['|   41 |', '|   33 |', '|  165 |', '|  152 |']
algos = ['|   41 |', '|   33 |', '|  165 |']

dateList = []
rateList = [[] for x in xrange(0,len(algos))]
for filename in glob.glob('RatesInfo*.txt'):
    datetimeString = filename[filename.find('0'):filename.rfind('.txt')]
    day = int(datetimeString[0:2])
    month = int(datetimeString[3:5])
    hour = int(datetimeString[6:8])
    minute = int(datetimeString[9:11])
    geneva = pytz.timezone("Europe/Amsterdam")
    naiveDate = datetime(2016, month, day+1, hour, minute)
    date = geneva.localize(naiveDate)
    #print "local: ", date
    dateList.append(date)
    #dateList.append(date.astimezone(pytz.utc))
    with open(filename) as f:
        index = 0
        for line in f:
            for algo in algos:
                if algo in line:
                    startPos = line.find(algo)+len(algo)
                    rate = int(line[startPos:line.find('|', startPos)])
                    rateList[index].append(rate)
                    index += 1

#for date, rate33, rate41, rate165 in zip(dateList, rateList[1], rateList[0], rateList[2]):
    # print date, rate33, rate41, rate165

x = [date2num(date.astimezone(pytz.utc)) for date in dateList]

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


