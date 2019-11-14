import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

if GPIO.input(7) == False:
    os.system("sudo python3 /home/pi/Camera/camera_script.py")
    os.system("/usr/bin/tvservice -o")
elif GPIO.input(7) == True and GPIO.input(13) == True:
    pass
else:
    while True:
        os.system("raspistill -o /home/pi/Desktop/image.jpg -t 60000")


