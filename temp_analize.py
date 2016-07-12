#!/usr/bin/env python3
# fish tank temp data analizer
# thomas & dad
# 2016 07 08
# todos: max mins and/or trends,
# maybe: graph temps & overlay,

### imports
import csv
import statistics
import logging
import logging.handlers
import numpy as np
import matplotlib.pyplot as plt


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
LOG_FILENAME = 'temp_analize.log'
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

#with open('/home/pi/fishtank/fishtemp.log') as csvfile:
with open('data.example') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=" ")
    dates = []
    times = []
    temps_c = []
    temps_f = []
    statuss = []
    dates0 = []
    times0 = []
    msgs0 = []
    for row in readCSV:
        if row[3] == 'celcius':
            dates.append(row[0])
            times.append(row[1])
            temps_c.append(float(row[4]))
            temps_f.append(float(row[7]))
            statuss.append(row[9])
        else:
            dates0.append(row[0])
            times0.append(row[1])
            msgs0.append(row[3])

#    print(dates)
#    print(times)
#    print(temps_c)
#    print(temps_f)
#    print(statuss)
    high = max(temps_f)
    low = min(temps_f)
    avg = statistics.mean(temps_f)
    var = statistics.variance(temps_f)
    std = statistics.stdev(temps_f)
    print(low, high, avg, var, std)

    t = np.arange(len(temps_f))
    h = np.ones((len(temps_f)), dtype=int) * 76
    l = np.ones((len(temps_f)), dtype=int) * 79
    plt.title('Fish Tank Temperature')
    plt.grid(True)
    plt.ylabel('temp F')
#    plt.axis([1, len(temps_f), 75, 80])
    plt.ylim(75, 80)
    plt.plot(t, temps_f, 'b-', t, l, 'r-', t, h,'r-')
#    plt.annotate('
    plt.show()



