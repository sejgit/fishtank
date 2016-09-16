#!/usr/bin/env python3
# fish tank scheduler & data collector
# thomas & dad
# 2016 06 20
# 2016 06 21 update for logging
# 2016 07 05 added temp prob & overlay to camera
# 2016 07 06 changed logging to complex form
# 2016 07 07 add temperature logging
# 2016 07 17 incorporate temp analysis & plot & external web
# 2016 07 18 change y axis & command line parse
# 2016 07 18 add args for -test -dir -plotonly
# 2016 07 19 prowl warnings & status
# 2016 07 20 fix plots
# 2016 07 21 clean-up .paul files to .ssh
# 2016 09 12 moved to agg away from X
# 2016 09 15 move temp parameters to work with new heater

# todos: max mins and/or trends
# maybe: button to turn light on at will, auto feeder

###
### imports and parse args
###

### imports
import datetime as dt
import pandas as pd
# import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.dates as md
# import matplotlib.ticker as ticker
# import matplotlib.cbook as cbook
import schedule
import time
import logging
import logging.handlers
import os
import sys
import glob
import subprocess
import paul

# parsing
import argparse

parser = argparse.ArgumentParser(
        description='Fishtank control & data aquisition')
parser.add_argument('-t', '--test', action='store_true',
                    help='turn on testing environment')
parser.add_argument('-p', '--plotonly', action='store_true',
                    help='plot and exit')
parser.add_argument('-d', '--dir',
                    help='home directory')
args = parser.parse_args()

if args.dir:
        dir = os.path.join(args.dir, '')
else:
        dir = '/home/pi/fishtank/'

if os.path.isdir(dir):
        print("\n" + dir + "   ***using directory***\n")
else:
        print("\n" + dir + "   ***not a dir***\n")
userdir = os.path.expanduser("~")

# hardware imports
if not args.test:
        from gpiozero import LED


###
### get logging going
###

# set up a specific logger with desired output level
LOG_FILENAME = dir + 'fishtank.log'

logger = logging.getLogger('FishTankLogger')

# add the rotating log message handler
fh = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=100000, backupCount=5)
if args.test:
        logger.setLevel(logging.DEBUG)
        fh.setLevel(logging.DEBUG)
else:
        logger.setLevel(logging.INFO)
        fh.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)


###
### get temperature logging going
###

# set up temp logger with desired output level
TEMP_LOG_FILENAME = dir + 'fishtemp.log'

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
logger.info('using directory  ' + dir)
logger.info('testing = ' + str(args.test))
if args.plotonly:
        logger.info('***plotonly***')
else:
        templogger.info('***start program')
        templogger.info('testing = ' + str(args.test))


###
### variables
###

# relay variables
if not args.test:
    relay1 = LED(17)
    relay2 = LED(18)
start = dt.time(5, 30)
start_str = str(start)[:5]
end = dt.time(20, 45)
end_str = str(end)[:5]

# temp prob set-up and vars
if not args.test:
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'


temp_f_hi = 79.5
temp_f_lo = 75.5
temp_c_test = 26

# prowl vars
try:
    p = paul.Paul()

    apikey1 = ""
    with open(os.path.join(userdir, ".ssh/.paul1"), "r") as f:
            apikey1 = f.read()
            apikey1 = apikey1.strip()

    apikey2 = ""
    with open(os.path.join(userdir, ".ssh/.paul2"), "r") as f:
            apikey2 = f.read()
            apikey2 = apikey2.strip()

except IOError:
    logger.error("Could not read prowl api file")


###
### defined functions
###

# paul prowl push def
def prowl(event, description, pri=None):
        try:
            p = paul.Paul()

            """
            p.push(apikey,
                   args.name,
                   args.event,
                   args.description,
                   url=args.url,
                   priority=args.priority)
            """

            # prowl push to sej
            p.push(apikey1,
                   'Fishtank',
                   event,
                   description,
                   url=None,
                   priority=pri)

            # prowl push to tej
            p.push(apikey2,
                   'Fishtank',
                   event,
                   description,
                   url=None,
                   priority=pri)
            
        except IOError:
            logger.error('prowl error')
        return

# temp prob def
def read_temp_raw():
        if not args.test:
                catdata = subprocess.Popen(['cat',device_file],
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                out,err = catdata.communicate()
                out_decode = out.decode('utf-8')
                lines = out_decode.split('\n')
        else:
                lines = ''
        return lines

def read_temp():
        if not args.test:
            lines = read_temp_raw()
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = read_temp_raw()
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
        else:
            temp_c = temp_c_test
            temp_f = temp_c * 9.0 / 5.0 + 32.0

        if temp_f > temp_f_hi:
            status = 'hi'
        elif temp_f < temp_f_lo:
            status = 'lo'
        else:
            status = 'ok'
        return temp_c, temp_f, status

# push temp status to prowl
def pushtempstatus():
    if "status_old" not in pushtempstatus.__dict__: pushtempstatus.status_old = 'first run'
    deg_c, deg_f, status = read_temp()
    if status != pushtempstatus.status_old:
        prowl('temperature ', (" *** " + status + " " + str(deg_f) + ' ***'), 0)
        pushtempstatus.status_old = status
    return

# relay def
def relay1_on():
    if not args.test:
        relay1.off()
    logger.info('relay1_on')
    return

def relay1_off():
    if not args.test:
        relay1.on()
    logger.info('relay1_off')
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
        while True:
            try:
                ### pull in log fishtemp.log file into pandas
                logger.debug('tempanalysis start')
                timestamp = dt.datetime.now()
                pdinp = pd.read_csv(TEMP_LOG_FILENAME, header=None,
                                    names=['datestamp','type',
                                           'status', 'temp_C', 'temp_F'],
                                    index_col=0, parse_dates = True,
                                    skipinitialspace=True)
                logger.debug('pd.read_csv done')
                pdinp = pdinp.dropna()
                logger.debug('pdinp.dropna done')
                pdinp.plot(title='FishTank Temperature', linewidth=.3,
                           kind='line',grid=True, y='temp_F',
                           ylim=[temp_f_lo, temp_f_hi])
                logger.info('plot done')
                fig = plt.gcf()
                fig.suptitle('Fishtank Temperature',
                             fontsize=20)
                logger.debug('fig done')
                ax = fig.add_subplot(111)
                logger.debug('subplot done')
                ax.set_title(timestamp.strftime('%b-%d-%Y %H:%M'),
                             fontsize=14)
                ax.xaxis.set_major_formatter(md.DateFormatter('%b-%d'))
                ax.set_xlabel(timestamp.strftime('%Y'), fontsize=16)
                ax.set_ylabel('temp_F', fontsize=16)
                logger.debug('axis format done')
                fig.savefig(dir + 'plot.png')
                if args.plotonly:
                    pass
                    plt.show()
                logger.info('tempanalysis done')
                break
            except Exception as ex:
                logger.error('tempanalysis error')
                template = "exception type {0} occured. Arguments:\n{1!r}"
                logger.error(template.format(type(ex).__name__, ex.args))
                break
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
    schedule.every(10).minutes.do(templog)    # log temp to templogger
    schedule.every().day.do(dailylog)    # daily log temp to logger & temp logger
    schedule.every(10).minutes.do(tempanalysis) # analyse and graph temperature data
    schedule.every(15).minutes.do(pushtempstatus) # push temperature status to prowl
    return

###
### main loop
###

def main():
    scheduling()
    timestamp = dt.datetime.now().time()
    logger.info('nowtime ='+ str(timestamp)[:5])

    # start or stop light/bubbles on first run
    if start <= timestamp <= end:
        logger.info('start relay1_on')
        relay1_on()
    else:
        logger.info('start relay1_off')
        relay1_off()

    # log & push temp on first run
    dailylog()
    pushtempstatus()
    hb = "*"

    while True:
        schedule.run_pending()
        try:
            time.sleep(60) # wait one minute
            hb = heartbeat(hb)
            deg_c, deg_f, status = read_temp()

            # overlay text onto RPi camera
            if not args.test:
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
    return


if __name__== '__main__':
    if args.plotonly:
        # prowl('test', 'plotonly', 0)
        tempanalysis()
    else:
        main()
    exit()

