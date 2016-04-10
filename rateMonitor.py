#!/bin/python

from datetime import datetime, timedelta
import subprocess
import time
import zipfile
import glob
import os

while True:

    zipFilename = 'rateLogs_' + datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    zf = zipfile.ZipFile('%s.zip' % (zipFilename), "w", zipfile.ZIP_DEFLATED)
    filenameStart = 'rates_'
    timeDelta = timedelta(hours=1)
    for filename in glob.glob(filenameStart + '*'):
        datetimeString = filename[filename.find(filenameStart)+len(filenameStart):]
        year = int(datetimeString[0:4])
        month = int(datetimeString[4:6])
        day = int(datetimeString[6:8])
        hour = int(datetimeString[9:11])
        minute = int(datetimeString[11:13])
        date = datetime(year, month, day, hour, minute)

        if (datetime.utcnow()-date) > timeDelta:
            zf.write(filename)
    zf.close()
    # Removing those files separately to be protected from unexpected crashes.
    for filename in glob.glob(filenameStart + '*'):
        datetimeString = filename[filename.find(filenameStart)+len(filenameStart):]
        year = int(datetimeString[0:4])
        month = int(datetimeString[4:6])
        day = int(datetimeString[6:8])
        hour = int(datetimeString[9:11])
        minute = int(datetimeString[11:13])
        date = datetime(year, month, day, hour, minute)

        if (datetime.utcnow()-date) > timeDelta:
            os.remove(filename)

    time.sleep(5)

    filename = 'rates_' + datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    f = open(filename, 'w')
    subprocess.call(['tdf', 'run', 'rate_counters_menu_v4', 'gt_mp7.1'], stdout=f)
    time.sleep(5*60)

