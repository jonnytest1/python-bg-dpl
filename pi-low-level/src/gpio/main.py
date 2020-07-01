# pylint: disable=import-error
import RPi.GPIO as GPIO

from customlogging import logKibana

pinnr = 21
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinnr, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)


def main(method, path, data, request):

    logKibana(level="DEBUG", msg="calling fan control",
              args=dict(enable=(data == "enablegpio")))

    if data == "enablegpio":
        print("enable "+str(pinnr))
        GPIO.output(pinnr, GPIO.HIGH)
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(16, GPIO.HIGH)
    else:
        GPIO.output(pinnr, GPIO.LOW)
        GPIO.output(20, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
        print("disable "+str(pinnr))

    print(method, path, data)
    return "hallo"
