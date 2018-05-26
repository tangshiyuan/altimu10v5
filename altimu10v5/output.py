import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pin1 = 17 # pin 11 on the RP board
pin2 = 27
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)

while 1:

    GPIO.output(pin1, (GPIO.HIGH))
    GPIO.output(pin2, (GPIO.HIGH))
    
    print("on")

    time.sleep(1)

    GPIO.output(pin1, (GPIO.LOW))
    GPIO.output(pin2, (GPIO.LOW))
    
    print("off")
    
    time.sleep(1)