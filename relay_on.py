
from gpiozero import LED
from time import sleep

relay1 = LED(17)
relay2 = LED(18)


relay2.on()
sleep(30)
relay2.off()

