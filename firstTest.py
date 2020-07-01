import os
import time
import threading
import pifacecad

print("test sersdf")
def start_camera(start_mode='camera'):
    cad = pifacecad.PiFaceCAD()

    switchlistener = pifacecad.SwitchEventListener(chip=cad)
    switchlistener.register(0, pifacecad.IODIR_ON, next_mode)
    switchlistener.register(1, pifacecad.IODIR_ON, option1)
    switchlistener.register(2, pifacecad.IODIR_ON, option2)
    switchlistener.register(3, pifacecad.IODIR_ON, option3)
    # switchlistener.register(4, pifacecad.IODIR_ON, exit)
    switchlistener.register(5, pifacecad.IODIR_ON, take_picture)
    switchlistener.register(6, pifacecad.IODIR_ON, previous_option)
    switchlistener.register(7, pifacecad.IODIR_ON, next_option)

    cad.lcd.display_off()
    cad.lcd.blink_off()
    cad.lcd.cursor_off()
    cad.lcd.clear()
    cad.lcd.backlight_on()

    splash_screen(cad)

    global camera
    camera = Camera(cad, start_mode)
    camera.current_mode['option'].enter()
    camera.update_display()
    cad.lcd.display_on()

    global should_i_exit
    should_i_exit = threading.Barrier(2)
    switchlistener.activate()
    should_i_exit.wait()
    switchlistener.deactivate()
    cad.lcd.clear()
    cad.lcd.backlight_off()
    print("Good-bye!")