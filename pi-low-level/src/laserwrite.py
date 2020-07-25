import sys
from time import sleep
# pylint: disable=import-error
import RPi.GPIO as GPIO
words = ""


enableDisablePin = 20
topDownPin = 27
rightLeftPin = 17
wallDistance = 50  # cm

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(enableDisablePin, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

print("laser pin "+str(enableDisablePin))

for i in range(1, len(sys.argv)):
    words = words+sys.argv[i]+" "

print(words)
print("\nResult:", "done")


def transformPositionToAngles(positionXY):
    return (positionXY[0], positionXY[1])


def writeletter(offset, char):
    GPIO.output(enableDisablePin, GPIO.HIGH)
    GPIO.output(21, GPIO.HIGH)
    GPIO.output(16, GPIO.HIGH)
    print(str(offset) + " " + char)

    sleep(1)
    #GPIO.output(enableDisablePin, GPIO.LOW)
    sleep(1)


offset = 0
for char in words:
    writeletter(offset, char)
    offset += 20
