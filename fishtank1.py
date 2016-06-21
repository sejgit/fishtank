# fish tank scheduler & data collector
# thomas & dad
# 2016 06 20

import schedule
import time
import datetime
from gpiozero import LED
import logging

logging.basicConfig(filename='fishtank.log',level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.info('start program')

relay1 = LED(17)
relay2 = LED(18)
start = datetime.time(6)
start_str = str(start)[:5]
end = datetime.time(21,28)
end_str = str(end)[:5]


def relay1_on():
    relay1.off()
    logging.debug('relay1_on')
    return

def relay1_off():
    relay1.on()
    logging.debug('relay1_off')
    return

schedule.every().day.at(start_str).do(relay1_on)
schedule.every().day.at(end_str).do(relay1_off)

timestamp = datetime.datetime.now().time()
logging.info('timestamp='+ str(timestamp)[:5])

if start <= timestamp <= end:
    relay1_on()
    logging.info('start relay1_on')
else:
    relay1_off()
    logging.info('start relay1_off')


while True:
    schedule.run_pending()
    try:
        time.sleep(60) # wait one minute
    except KeyboardInterrupt:
        print('\n\nKeyboard exception. Exiting.\n')
        logging.info('keyboard exception')
        exit()
    except:
        logging.info('end program')
        exit()



