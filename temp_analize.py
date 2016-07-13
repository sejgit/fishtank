#!/usr/bin/env python3
# fish tank temp data analizer
# thomas & dad
# 2016 07 08
# todos: max mins and/or trends,
# maybe: graph temps & overlay,

### imports
import datetime as dt
import csv
import statistics
import logging
import logging.handlers
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.cbook as cbook


### get logging going
time_format = '%Y-%m-%d %H:%M:%S'
# set up a specific logger with desired output level
LOG_FILENAME = 'temp_analize.log'
logger = logging.getLogger('FishTankTempLogger')
logger.setLevel(logging.DEBUG)

# add the rotating log message handler
fh = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20000, backupCount=5)
fh.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt=time_format)
fh.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)

logger.info('***start program')


pdinp = pd.read_csv('fishtemp.log', header=None, names=['date', ' )
print(pdinp)






"""
print(times)
print(temps_c)
print(temps_f)
print(statuss)
high = max(temps_f)
low = min(temps_f)
avg = statistics.mean(temps_f)
var = statistics.variance(temps_f)
std = statistics.stdev(temps_f)
print(low, high, avg, var, std)

    t = np.arange(len(temps_f))
    h = np.ones((len(temps_f)), dtype=int) * 76
    l = np.ones((len(temps_f)), dtype=int) * 79

    fig, ax = plt.subplots()
    plt.title('Fish Tank Temperature')
    plt.grid(True)
    plt.ylabel('temp F')
    plt.ylim(75, 80)
#    plt.plot(t, temps_f, 'b-', t, l, 'r-', t, h,'r-')

    ax.plot(dateobject, temps_f, 'b-')
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(days)

    datemin = datetime.date(dateobject.date.min().year, 1, 1)
    datemax = datetime.date(dateobject.date.max().year +1, 1, 1)
    ax.set.xlim(datemin, datemax)

    plt.show()

"""

