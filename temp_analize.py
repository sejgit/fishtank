#!/usr/bin/env python3
# fish tank temp data analizer
# thomas & dad
# 2016 07 08
# 2016 07 14 using pandas
# todos: max mins and/or trends,
# maybe: graph temps & overlay,

### imports
import datetime as dt
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
###


logger.info('***start program')


### pull in log fishtemp.log file into pandas
pdinp = pd.read_csv('fishtemp.log', header=None, names=['datestamp', 'type', 'status', 'temp_C', 'temp_F'], index_col=0, parse_dates = True, skipinitialspace=True)

print(pdinp)
print(pdinp.index)

pdinp2 = pdinp.copy()
# pdinp2 = pdinp2[pdinp2['status'].isin(['ok', 'hi', 'lo'])]
pdinp2 = pdinp2['status'].isin(['ok', 'hi', 'lo'])

print(pdinp2)


pdinp.plot(ylim=[15,80])
fig = plt.gcf()
fig.savefig('plot.png')
plt.show()



