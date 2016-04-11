#!/bin/python
import glob
from datetime import datetime, timedelta
import pytz
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.dates import date2num
import argparse
import time
import sys

desc = "Tool to extract rates from tdf dumps"

parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--filename', type=str, default='rates_', help='Generic part of TDF dump filename (i.e. part excluding timestamp).')
parser.add_argument('--path', type=str, default='', help='Path to folder with TDF dumps.')
parser.add_argument('--outpath', type=str, default='', help='Folder to store plots in.')
parser.add_argument('--continuous', default=False, action='store_true', help='Whether to run in continuous mode.')
opts = parser.parse_args()

algos = ['|   41 |', '|   33 |', '|  165 |', '|  140 |', '|  154 |']

if opts.path == '':
    path = ''
elif opts.path[-1] != '/':
    path = opts.path + '/'
else:
    path = opts.path

if opts.outpath == '':
    outpath = opts.outpath
else:
    outpath = opts.outpath + '/'

timeDelta = timedelta(minutes=10)
#timeDelta = timedelta(minutes=25)
while True:
    dateList = []
    rateList = [[] for x in xrange(0,len(algos))]
    for filename in glob.glob(path + opts.filename + '*'):
        datetimeString = filename[filename.find(opts.filename)+len(opts.filename):]
        year = int(datetimeString[0:4])
        month = int(datetimeString[4:6])
        day = int(datetimeString[6:8])
        hour = int(datetimeString[9:11])
        minute = int(datetimeString[11:13])
        second = int(datetimeString[13:15])
        date = datetime(year, month, day, hour, minute, second)
        if (datetime.utcnow()-date) > timeDelta:
            continue
        dateList.append(date)
        with open(filename) as f:
            index = 0
            for line in f:
                for algo in algos:
                    if algo in line:
                        #print index, algo, line
                        startPos = line.find(algo)+len(algo)
                        rate = int(line[startPos:line.find('|', startPos)])
                        #print rate
                        rateList[index].append(rate)
                        index += 1
    #print dateList, rateList
    
    x = [date2num(date) for date in dateList]

    fig = plt.figure()
    graph = fig.add_subplot(111)
    try:
        graph.plot(x, rateList[0], 'ro', x, rateList[1], 'bs', x, rateList[2], 'y*', x, rateList[3], 'mp', x, rateList[4], 'g^')
        graph.set_xticks(x)

        legend = graph.legend(['SingleEG5', 'SingleMuOpen', 'SingleJet16', 'SingleJet36', 'BPTX AND'], numpoints=1, loc='upper left')
        
        graph.set_xticklabels(
            [date.strftime("%H:%M:%S") for date in dateList]
            )
        fig.autofmt_xdate()
        plt.ylabel('Rate [Hz]')
        plt.savefig(outpath + 'uGTrates.png', bbox_inches='tight')
    
        plt.yscale('log', nonposy='clip')
        plt.savefig(outpath + 'uGTrates_log.png', bbox_inches='tight')
    except ValueError as e:
        print "Value error: {0}".format(e)
        print "[ERROR]: Plotting failed."
        print 'x', x, 'eg5', rateList[0], len(x), len(rateList[0])
        print 'x', x, 'muopen', rateList[1], len(x), len(rateList[1])
        print 'x', x, 'jet16', rateList[2], len(x), len(rateList[2])
        print 'x', x, 'jet36', rateList[3], len(x), len(rateList[3])
        print 'x', x, 'bptx', rateList[4], len(x), len(rateList[4])
    
    if opts.continuous is True:
        time.sleep(15*1)
    else:
        break

