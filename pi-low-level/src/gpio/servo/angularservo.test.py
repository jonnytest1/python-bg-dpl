from time import sleep
from gpiozero import AngularServo

s = AngularServo(17, min_angle=-90, max_angle=90, min_pulse_width=0.5 /
                 1000, max_pulse_width=2.5/1000, frame_width=20/1000)
