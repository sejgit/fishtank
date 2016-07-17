#!/usr/bin/env python3
# fish tank scheduler & data collector
# thomas & dad
# 2016 06 20
# 2016 06 21 update for logging
# 2016 07 05 added temp prob & overlay to camera
# 2016 07 06 changed logging to complex form
# 2016 07 07 add temperature logging
# 2016 07 17 incorporate temp analysis & plot & external web
# todos: log errors, prowl errors, max mins and/or trends
# maybe: button to turn light on at will, auto feeder

### imports
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
# import matplotlib.cbook as cbook
import schedule
import time
from gpiozero import LED
import logging
import logging.handlers
import os
import sys
import glob
import subprocess

###
### get logging going
###

# set up a specific logger with desired output level
LOG_FILENAME = '/home/pi/fishtank/fishtank.log'
logger = logging.getLogger('FishTankLogger')
logger.setLevel(logging.DEBUG)

# add the rotating log message handler
fh = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20000, backupCount=5)
fh.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)


###
### get temperature logging going
###

# set up temp logger with desired output level
TEMP_LOG_FILENAME = '/home/pi/fishtank/fishtemp.log'
templogger = logging.getLogger('FishTempLogger')
templogger.setLevel(logging.DEBUG)

# add the rotating log message handler
tfh = logging.handlers.RotatingFileHandler(TEMP_LOG_FILENAME, maxBytes=0, backupCount=5)
tfh.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
tempformatter = logging.Formatter(fmt='%(asctime)s, %(levelname)s, %(message)s', datefmt='%Y-%m-%dT%H:%M:%S')
tfh.setFormatter(tempformatter)

# add the handlers to the logger
templogger.addHandler(tfh)


logger.info('***start program')
templogger.info('***start program')

###
### variables
###

# relay variables
relay1 = LED(17)
relay2 = LED(18)
start = dt.time(5, 30)
start_str = str(start)[:5]
end = dt.time(20, 45)
end_str = str(end)[:5]

# temp prob set-up and vars
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
temp_f_hi = 80
temp_f_lo = 75

# prowl vars
daily = dt.time(12, 00)


###
### defined functions
###

# temp prob def
def read_temp_raw():
	catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out,err = catdata.communicate()
	out_decode = out.decode('utf-8')
	lines = out_decode.split('\n')
	return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        if temp_f > temp_f_hi:
            status = 'hi'
        elif temp_f < temp_f_lo:
            status = 'lo'
        else:
            status = 'ok'
        return temp_c, temp_f, status


# relay def
def relay1_on():
    relay1.off()
    logger.debug('relay1_on')
    return

def relay1_off():
    relay1.on()
    logger.debug('relay1_off')
    return


# writing of temps
def templog():
    deg_c, deg_f, status = read_temp()
    templogger.info('{2}, {0:.2f}, {1:.2f}'.format(deg_c, deg_f, status))
    return

def dailylog():
    deg_c, deg_f, status = read_temp()
    logger.info('celcius {0:.2f}  fahrenheit {1:.2f}  {2}'.format(deg_c, deg_f, status))
    templogger.info('{2}, {0:.2f}, {1:.2f}'.format(deg_c, deg_f, status))
    return


# temp data analysis
def tempanalysis():
        ### pull in log fishtemp.log file into pandas
        pdinp = pd.read_csv('fishtemp.log', header=None, names=['datestamp', 'type', 'status', 'temp_C', 'temp_F'], index_col=0, parse_dates = True, skipinitialspace=True)
        pdinp = pdinp.dropna()
        fig = plt.gcf()
        ax = fig.add_subplot(111)
        pdinp.plot(title='FishTank Temperature', kind='line', grid=True, y='temp_F', ylim=[75,80])
        ax.xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
        fig.savefig('plot.png')
        #plt.show()
        return

# heartbeat function
def heartbeat(ast):
    if ast==" ":
        ast = "*"
    else:
        ast = " "
    return ast


###
### first run items
###

def scheduling():
    # set scheduled events
    schedule.every().day.at(start_str).do(relay1_on)  # light/bubbler ON in morning
    schedule.every().day.at(end_str).do(relay1_off)   # light/bubler OFF at night
    logger.info('start light on='+ start_str)
    logger.info('end light off='+ end_str)
    schedule.every(15).minutes.do(templog)    # log temp to templogger
    schedule.every().day.do(dailylog)    # daily log temp to logger & temp logger
    schedule.every(30).munutes.do(tempanalysis) # analyse and graph temperature data
    return

###
### main loop
###

def main():
    scheduling()
    # timestamp
    timestamp = dt.datetime.now().time()
    logger.info('nowtime ='+ str(timestamp)[:5])

    # start or stop light/bubbles on first run
    if start <= timestamp <= end:
        relay1_on()
        logger.info('start relay1_on')
    else:
        relay1_off()
        logger.info('start relay1_off')

    # log temp on first run
    dailylog()
    hb = "*"

    while True:
        schedule.run_pending()
        try:
            time.sleep(60) # wait one minute
            hb = heartbeat(hb)
            deg_c, deg_f, status = read_temp()

            # overlay text onto RPi camera
            with open('/dev/shm/mjpeg/user_annotate.txt', 'w') as f:
                f.write('celcius {0:.2f}  fahrenheit {1:.2f}  {2}'.format(deg_c, deg_f, status+hb))
            f.closed

        except KeyboardInterrupt:
            print('\n\nKeyboard exception. Exiting.\n')
            logger.info('keyboard exception')
            exit()

        except:
            logger.info('program end:', sys.exc_info()[0])
            exit()


if __name__== '__main__':
    main()
    exit()
