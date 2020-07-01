from time import sleep
from gpiozero import AngularServo

s = AngularServo(17, min_angle=-90, max_angle=90)

s.angle = 60
sleep(8)
s.angle = -60
sleep(8)
s.close()
