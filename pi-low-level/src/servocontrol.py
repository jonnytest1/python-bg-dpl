from time import sleep
# pylint: disable=import-error
import RPi.GPIO as GPIO

servoPIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50)

p.start(5)


def setangle(angle):
    try:
        p.ChangeDutyCycle(angle)
        sleep(10)
        p.ChangeDutyCycle(0)
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
    print(angle)
