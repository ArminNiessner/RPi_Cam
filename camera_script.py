#!/usr/bin/python3

import os
from time import sleep
from datetime import datetime
import picamera
import glob
import RPi.GPIO as GPIO
import picam_mod

GPIO.setmode(GPIO.BOARD)
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


set_file = open("/home/pi/Desktop/settings.txt", "r")
NP = int(set_file.readline().split("=")[1])
PWT = int(set_file.readline().split("=")[1])
NPX = int(set_file.readline().split("=")[1])
DTP = int(set_file.readline().split("=")[1])
VWT = int(set_file.readline().split("=")[1])
NV = int(set_file.readline().split("=")[1])
DT =  int(set_file.readline().split("=")[1])
crot = int(set_file.readline().split("=")[1])
w = int(set_file.readline().split("=")[1])
h = int(set_file.readline().split("=")[1])
threshold = int(set_file.readline().split("=")[1])
sensitivity = int(set_file.readline().split("=")[1])
shutdown_datetime = set_file.readline().split("=")[1]
night_hours = set_file.readline().split("=")[1].split(",")
night_hours = list(map(int, night_hours))

PTH_i = "/home/pi/Camera/"

cres = (w, h) # image resolution
##############

print("VID: {}, MD: {}, TiSt: {}".format(VID,MD,TiSt))
print("Shutdown at: {}, night hours from {} to {}".format(shutdown_datetime, night_hours[0], night_hours[-1]))

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
        zeros = digits(M+1) * "0"
        for i, filename in enumerate(camera.capture_continuous(PTH+'/'+zeros+str(M+1)+'-'+'image{timestamp:%H-%M-%S}-{counter:04d}.jpg')):
            if TiSt == True:
                timeStamp(filename)
            sleep(wt)
            if i ==(N-1):
                break
    print("Picture(s) "+zeros+str(M+1)+" taken.")

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
    
def digits(m):
    dig1 = NPX
    count1 = 0
    while(dig1 > 0):
        dig1 = dig1 // 10
        count1 += 1
    dig2 = m
    count2 = 0
    while(dig2 > 0):
        dig2 = dig2 // 10
        count2 += 1
    zeros = count1 - count2
    return zeros
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

