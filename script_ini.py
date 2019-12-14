import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

set_file = open("/home/pi/Desktop/settings.txt", "r")
for i in [1,2,3,4,5,6,7]:
    set_file.readlne()
crot = int(set_file.readline().split("=")[1])

if GPIO.input(7) == False:
    os.system("sudo python3 /home/pi/Camera/camera_script.py")
    os.system("/usr/bin/tvservice -o")
elif GPIO.input(7) == True and GPIO.input(13) == True:
    pass
else:
    while True:
        os.system("raspistill -o /home/pi/Desktop/image.jpg -rot {} -t 60000".format(crot))


