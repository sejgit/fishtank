#!/usr/bin/env python3
# fish tank temp data analizer
# thomas & dad
# 2016 07 08
# todos: max mins and/or trends,
# maybe: graph temps & overlay,

### imports
import csv
import logging
import logging.handlers

"""
import schedule
import time
import datetime
from gpiozero import LED
import os
import sys
import glob
import subprocess
"""
### get logging going

# set up a specific logger with desired output level
LOG_FILENAME = '/home/pi/fishtank/temp_analize.log'
logger = logging.getLogger('FishTankTempLogger')
logger.setLevel(logging.DEBUG)

# add the rotating log message handler
fh = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20000, backupCount=5)
fh.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)

logger.info('***start program')

with open('/home/pi/fishtank/fishtemp.log') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=" ")
    dates = []
    times = []
    temps_c = []
    temps_f = []
    statuss = []
    for row in readCSV:
        if row[2] == 'celcius':
            date = row[0]
            time = row[1]
            temp_c = row[4]
            temp_f = row[6]
            status = row[7]
            dates.append(date)
            times.append(time)
            temps_c.append(temp_c)
            temps_f.append(temp_f)
            statuss.append(status)
        else:
            print row[2]

    print(dates)
    print(times)
    print(temps_c)
    print(temps_f)
    print(statuss)


