# pylint: disable=import-error
import RPi.GPIO as GPIO
from servocontrol import p
from customlogging import logKibana
from time import sleep
#import sys
# from servolib import p
#servoPIN = 17
#sys.stdout = open("/home/jonathan/python/log.log", "a")
#servo = AngularServo(17, min_pulse_width=2.5, max_pulse_width=12.5)


def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)


def main(method, path, data, request):
    frequency = translate(int(data), 0, 100, 2.5, 12.5)

    # 180 degrees
    logKibana("DEBUG", "setting frequency", args=dict(angle=frequency))
    try:
        p.ChangeDutyCycle(frequency)
        sleep(0.5)
        p.ChangeDutyCycle(0)
        p.stop()
    except KeyboardInterrupt:
        p.stop()
    return "hallo"
