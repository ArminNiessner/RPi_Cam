# RPi_Cam
Raspberry Pi Zero Camera with motion detection

## Special features
* take pictures or videos in a certain intverval
* take pictures or videos triggerd by motion
* adjustable sensitivity of motion detection
* suspend taking pictures/videos during night hours to save energy
* programamble shutdown at a certain time
* hardware-switch to change between pictures-videos, motion detection on-off, timestamp on-off, test mode-normal mode
* buttons for rebooting or shutting down the pi
* real-time clock to keep the time 

## Setup
1. flash sd card with raspbian image
2. create ssh and wpa_supplicant.conf files in boot partition to be able to connect to the pi over wifi
3. enable camera and i2c, and set timezone (sudo raspi-config)
4. set up the rtc (https://pimylifeup.com/raspberry-pi-rtc/ or https://www.raspberrypi-spy.co.uk/2015/05/adding-a-ds3231-real-time-clock-to-the-raspberry-pi/)
5. disable HDMI (saves 25mA), running: /usr/bin/tvservice -o (-p to re-enable). Add the line to /etc/rc.local to disable HDMI on boot
6. install imagemagick (sudo apt-get install imagemagick)
7. add the python files from this repository to /home/pi/Camera/
8. add the lines:
        * python3 /home/pi/Camera/camera_button_off.py &
        * python3 /home/pi/Camera/camera_button_rebo.py &
        * python3 /home/pi/Camera/camera_motion_script_switch &


