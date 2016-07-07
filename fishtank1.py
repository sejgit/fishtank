# fish tank scheduler & data collector
# thomas & dad
# 2016 06 20
# 2016 06 21 update for logging
# 2016 07 05 added temp prob & overlay to camera
# 2016 07 06 changed logging to complex form

# imports
import schedule
import time
import datetime
from gpiozero import LED
import logging
import logging.handlers
import os
import glob
import subprocess

# get logging going
# logging.basicConfig(filename='/home/pi/fishtank/fishtank.log', fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

# set up a specific logger with desired output level
LOG_FILENAME = '/home/pi/fishtank/fishtank.log'
logger.getLogger('FishTankLogger')
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

# relay variables
relay1 = LED(17)
relay2 = LED(18)
start = datetime.time(5, 30)
start_str = str(start)[:5]
end = datetime.time(20, 45)
end_str = str(end)[:5]

# temp prob set-up and vars
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# prowl vars
daily = datetime.time(12, 00)


base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
ast = "*"
x = 1

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
        return temp_c, temp_f

# relay def
def relay1_on():
    relay1.off()
    logger.debug('relay1_on')
    return

def relay1_off():
    relay1.on()
    logger.debug('relay1_off')
    return

# set schedule
schedule.every().day.at(start_str).do(relay1_on)
schedule.every().day.at(end_str).do(relay1_off)
logger.info('start light on='+ start_str)
logger.info('end light off='+ end_str)

# timestamp
timestamp = datetime.datetime.now().time()
logger.info('nowtime ='+ str(timestamp)[:5])

# start or stop light/bubbles on first run
if start <= timestamp <= end:
    relay1_on()
    logger.info('start relay1_on')
else:
    relay1_off()
    logger.info('start relay1_off')


# main loop
while True:
    schedule.run_pending()
    try:
        time.sleep(60) # wait one minute
        deg_c, deg_f = read_temp()
        if ast==" ":
            ast = "*"
        else:
            ast = " "
        with open('/dev/shm/mjpeg/user_annotate.txt', 'w') as f:
            f.write('celcius {0:.2f}  fahrenheit {1:.2f}  {2}'.format(deg_c, deg_f, ast))
            if x >= 60:
                x = 1
                logger.info('celcius {0:.2f}  fahrenheit {1:.2f}  {2}'.format(deg_c, deg_f, ast))
            else:
                x += 1
        f.closed
    except KeyboardInterrupt:
        print('\n\nKeyboard exception. Exiting.\n')
        logger.info('keyboard exception')
        exit()
    except:
        logger.info('end program')
        exit()



