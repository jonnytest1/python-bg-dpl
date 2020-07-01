#from servocontrol import setangle
from time import sleep
# pylint: disable=import-error
import RPi.GPIO as GPIO

# setangle(40)

# servo = AngularServo(17, min_angle=-90, max_angle=90,
#                   min_pulse_width=2.5/1000, max_pulse_width=12.5/1000)
servoPIN = 17


GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50)

p.start(2.5)

try:
    while True:
        print("servo cycle")
        p.ChangeDutyCycle(5)
        sleep(0.5)
        p.ChangeDutyCycle(7.5)
        sleep(0.5)
        p.ChangeDutyCycle(10)
        sleep(0.5)
        p.ChangeDutyCycle(12.5)
        sleep(0.5)
        p.ChangeDutyCycle(10)
        sleep(0.5)
        p.ChangeDutyCycle(7.5)
        sleep(0.5)
        p.ChangeDutyCycle(5)
        sleep(0.5)
        p.ChangeDutyCycle(2.5)
        sleep(0.5)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
