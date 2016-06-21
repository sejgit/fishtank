
from gpiozero import LED
from time import sleep

relay1 = LED(17)
relay2 = LED(18)


while True:
        relay1.on()
        relay2.off()
        sleep(1)
        relay1.off()
        relay2.on()
        sleep(1)

