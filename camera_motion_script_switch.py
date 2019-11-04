#!/usr/bin/python3

"""
Created on Mon Oct 28 16:57:50 2019

@author: armin


 Copyright (C) 2019  Armin Niessner
 
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program. If not, see <https://www.gnu.org/licenses/>.

"""

import os
from time import sleep
from datetime import datetime
import picamera
import glob
import RPi.GPIO as GPIO
import picam_mod

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

motionState = False
##############

if GPIO.input(13) == True:
    VID = True
else:
    VID = False
    
if GPIO.input(11) == True:
    MD = True
else:
    MD = False
    
if GPIO.input(12) == True:
    TiSt = True
else:
    TiSt = False
    
if GPIO.input(7) == True:
    NP=2  #Number of pictures
    PWT=3  #Time bewteen pictures in seconds
    NPX=10      #Number of picture series 
    DTP=2    #Interval between picture series in seconds-0 one series
    VWT=20  #Video length in seconds
    NV=2    #Number of videos
    DT=20    #Interval between videos in seconds
    
else:
    NP=3  #Number of pictures
    PWT=10  #Time bewteen pictures in seconds
    NPX=1000      #Number of picture series 
    DTP=2    #Interval between picture series in seconds-0 one series
    VWT=5*60  #Video length in seconds
    NV=2    #Number of videos
    DT=1*60    #Interval between videos in seconds 

PTH_i = "/home/pi/Camera/"

crot = 0 #camera rotation
cres = (3280, 2464) # image resolution
threshold = 10  #how much a pixel has to change by to be marked as "changed"
sensitivity = 20    #how many changed pixels before capturing an image, needs to be higher if noisy view
shutdown_datetime = "2019-10-21 18:40"
night_hours = [23, 0, 1, 2, 3, 4, 5, 6, 7]    #hours when no pictures should be taken
##############

def picts_md(wt,M,PTH,N,thh,sens):
    while True:
        check_shutdown()
        check_night()
        motionState = picam_mod.motion(thh, sens)
        print(motionState)
        if motionState:
            print("Smile for the camera!")
            picts(wt,M,PTH,N)
            break #

def picts(wt,M,PTH,N):

    with picamera.PiCamera() as camera:
        camera.resolution = cres
        camera.rotation = crot
        for i, filename in enumerate(camera.capture_continuous(PTH+'/'+str(M+1)+'-'+'image{timestamp:%H-%M-%S}-{counter:04d}.jpg')):
            if TiSt == True:
                timeStamp(filename)
            sleep(wt)
            if i ==(N-1):
                break
    print("Picture(s) taken.")

###############

def vids_md(ST,M,PTH,thh,sens):
    while True:
        check_shutdown()
        check_night()
        motionState = picam_mod.motion(thh, sens)
        print(motionState)
        if motionState:
            print("Smile for the camera!")
            vids(ST,M,PTH)
            break #
       

def vids(ST,M,PTH):
    with picamera.PiCamera() as camera:
        camera.rotation=crot
        ts=PTH+'/'+str(M+1)+"-"+datetime.now().strftime("%H-%M-%S")+".h264"
        camera.start_recording(ts)
        camera.wait_recording(ST)
        camera.stop_recording()
        print("DONE VIDEO")
##############
def wrtrun():
	with open(PTH_i + "NR.TXT","w") as f:          # create and open file in write mode
		f.write(str(0))                   # write "0" in file
        
def check_shutdown():
    str_datetime = str(datetime.now())[:16]
    if str_datetime == shutdown_datetime:
        print("Time to shut down")
        os.system("sudo shutdown -h now")
    else:
        pass
   
def check_night():
    while datetime.now().hour in night_hours:
        print("sleeping...")
        sleep(60)
        check_shutdown()
        
def timeStamp(filepath):
    str_datetime = str(datetime.now())[:19]
    os.system("/usr/bin/convert " + filepath + " -pointsize 102 -fill red -annotate +2300+2400 '" + str_datetime + "' " + filepath)
    
##############
def main():
    nrl=glob.glob(PTH_i + "*.TXT")
    if len(nrl)==0:        # if run for the first time -> no txt files
        wrtrun()
	
    with open(PTH_i + "NR.TXT","r") as f:
        for row in f:
            nk=int(row)
    NF=nk+1

    with open (PTH_i + "NR.TXT","w") as f:
        f.write(str(NF))

    PTH=PTH_i + "BOOT"+str(NF)
    os.mkdir(PTH)
    sleep(10)
    
    if VID==False:
        for np in range(NPX):
            if MD==True:
                picts_md(PWT,np,PTH,NP,threshold,sensitivity)
            else:
                picts(PWT,np,PTH,NP)
            if DTP>0:
                sleep(DTP)
            else:
                pass
            check_shutdown()
            check_night()
    else:
        for nv in range(NV):
            if MD==True:
                vids_md(VWT,nv,PTH,threshold,sensitivity)
            else:
                vids(VWT,nv,PTH)
            sleep(DT)
            check_shutdown()
            check_night()
	
    with open(PTH_i + "NRLOGS.TXT","w") as f:
        f.write(PTH+" process completed without interruptions")

    os.system("sudo shutdown -h now")  
##############
main()

