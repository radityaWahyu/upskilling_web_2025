from machine import Pin
from time import sleep

# inisilisasi pin 2 sebagai output
led = Pin(2,Pin.OUT)

while True:
    # led pada pin 2 hidup
    led.on()
    # tunggu sampai 1 detik
    sleep(0.5)
    
    # led pada pin 2 mati
    led.off()
    # tunggu sampai 1 detik
    sleep(0.5)
    
    