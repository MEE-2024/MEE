#Custom Imports
import celelib_v_0_3
import celelibloader_v_0_3

import time
import os
import sys
import numpy as np

#Alpaca Library Imports
from alpaca.camera import *
from alpaca.telescope import *
from alpaca.exceptions import *

import astropy.io.fits as fits
# random change

albert = Telescope('192.168.1.47:11111',0)
stacy = Camera('192.168.1.47:11111',0)
RA = albert.RightAscension
DEC = albert.Declination

def main_menu():
    #This function is the central hub for the user
    #Function finds out what type of input the user would like to input
    mm_flag = True
    while mm_flag == True:
        
        print("")
        print("""Make a Selection:
        1 - Slew to Position
        2 - Slew to Library Position
        3 - Slew to Home
        4 - Print Current DA/REC
        x - Exit Program""")

        choice = input(">")
        if choice == "1":
            #send to RA/DEC collection and validation
            print("Slew to Position")
            user_validation_station(choice)
            
        elif choice == "2":
            #send to Library lookup, collection and validation
            print("Slew to Library Position")
            user_validation_station(choice)
            
        elif choice == "3":
            print("Slew to Home")
            #send to validation and then home RA/DEC straight to mount movement control
            print(choice)
            user_validation_station(choice)

        elif choice == "4":
            #returns current RA/DEC
            print("Current RA/DEC: ")
            print(albert.RightAscension)
            print(albert.Declination)
            input("Press Enter To Return To Main Menu: ")
            
        elif choice.lower() == "x":
            print("Exit Program")
            #albert.Tracking = False
            #albert.Connected = False #Do I need this?
            print(albert.Tracking) #This is the only place where the tracking is shut off
            print(RA)
            print(DEC)
            mm_flag = False
            
        else:
            print("invalid input")
    
        
def user_validation_station(validate_choice):
    #This function takes users choice and determines what type of input validation is needed
    #Function then sends data to mount movement control as RA and DEC values
    user_choice = validate_choice
    print(user_choice)

    if user_choice == "1":
        deciding_location = True
        while deciding_location == True:
            RA_MAX = 24.0
            RA_MIN = 0.0
            DEC_MAX = 90.0
            DEC_MIN = -90.0
            RA = float(input("Please Enter Right Ascension Value (float): "))
            if RA >= RA_MIN and RA < RA_MAX :
                #limits of this if statement may need to be vars that can be altered per each location prog is being used
                #send to mount movement control
                print("Right Ascension Recieved")
            else:
                print("invalid response")
            DEC = float(input("Please Enter Declination Value (float): "))
            if DEC_MIN <= -90.0 and DEC_MAX >= 90.0:
                #limits of this if statement may need to be vars that can be altered per each location prog is being used
                #send to mount movement control
                print("Declination Recieved")
            else:
                print("invalid response")
            break
        #Send RA/DEC to mount control for slewing
        mount_movement_control(RA,DEC)
    
    elif user_choice == "2":
        print("Library of Coordinates")
        celelibloader_v_0_3.libraryloader()
        from celelibloader_v_0_3 import Ra,Dec
        mount_movement_control(Ra, Dec)

    elif user_choice == "3":
        #returns mount to 0/0
        #send RA and DEC to mount movement control
        print("choice 3")
        
        albert.SlewToCoordinatesAsync(RightAscension=10.0000000000, Declination=0.0000000000)
        print(f"RA = {albert.RightAscension}, DEC = {albert.Declination}")
        while(albert.Slewing):
            time.sleep(5)
            print("Doot... Doot... Doot...")

    else:
        print("AGGGGGGHHHHH!")


def mount_movement_control(RA, DEC):
    #USER_RA = RA
    #USER_DEC = DEC
    print("You are at mount movement control")
    print(RA)
    print(DEC)
    operation = True
    while operation is True:
        #Function moves telescope to desired location
        input("Press Enter to Begin Slew")
        #This is where the magic happens
        
        albert.SlewToCoordinatesAsync(RightAscension=RA, Declination=DEC)
        print(f"RA = {albert.RightAscension}, DEC = {albert.Declination}")
        #Checking when slew is finished every 1 sec
        while(albert.Slewing):
            time.sleep(1)
            albert.Tracking = True
            print(albert.RightAscension)
            print(albert.Declination)
            print("Doot... Doot... Doot...")
        #This is where a call to camera function would be
        print("Mount has been moved")
        print()
        print("""Would you like to continue?
        1 - Slew To New Location
        2 - Camera Operations
        x - Back To Main Menu""")
        user_slew_choice = input(">")
        if user_slew_choice == "1":
            main_menu()
        elif user_slew_choice == "2":
            print("Camera Controls")
            camera_control()
        #elif camera functions go here
        elif user_slew_choice.lower() == "x":
            print("Back To Main Menu")
            break
        else:
            print("returning to main menu")
            main_menu()
        

def camera_control():
    #The purpose of this function is to control camera connectivity, taking pictures and sending FITS data to data processing function
    stacy.Connected = True
    print(stacy.Connected)
    stacy.BinX = 1
    stacy.BinY = 1
    #Assure full frame after binning change
    stacy.StartX = 0
    stacy.StartY = 0
    stacy.NumX = stacy.CameraXSize // stacy.BinX #int type
    stacy.NumY = stacy.CameraYSize // stacy.BinY
    input("Press Enter to Continue")
    print(f"Current Camera State: {stacy.CameraState}")
    print(f"Sensor Name: {stacy.SensorName}, Sensor Type: {stacy.SensorType}")
    print(f"Current CCD Temp: {stacy.CCDTemperature}")
    #print(f"Current Camera Heat Sink Temp: {stacy.HeatSinkTemperature}")
    print(f"Cooler is on: {stacy.CoolerOn}")
    print(f"Current CCD Gain: {stacy.ElectronsPerADU}")
    print(f"CCD Pixel Size: X = {stacy.PixelSizeX}, Y = {stacy.PixelSizeY}")

    imgs_collected = input("Please Input the amount of continuous images you want taken")
    img_exposure_time = float(input("Please input exposure time (float)(sec): "))
    img_file_name = ""

    img_collected_count = 1
    while img_collected_count > imgs_collected:
        img_collected_count += 1
        stacy.StartExposure(img_exposure_time, True)
        while not stacy.ImageReady:
            time.sleep(0.5)
            print(f"Image Ready: {stacy.ImageReady}")
            print(f"Current Camera State: {stacy.CameraState}")
            #print(f"{stacy.PercentCompleted}")
        #stacy.StopExposure() #I don't think that this is needed when stacy.imageready is being used, automatically swithes camera to idle after while loop exit
        print(f"Max Camera ADU: {stacy.MaxADU}")
        input("Press Enter to Continue")

        img = stacy.ImageArray
        imginfo = stacy.ImageArrayInfo
        imgDataType = np.uint16
        print(f"Image Rank: {imginfo.Rank}")
        nda = np.array(img,dtype=imgDataType).transpose()

        hdr = fits.Header()
        hdr["Comment"] = "Fits (Flexible Image Transport System) format defined in Astronomy and"
        hdr["Comment"] = "Astrophysics Supplement Series v44/p363, v44/p371, v73/p359, v73/p365."
        hdr["Comment"] = "Contact the NASA Science Office of Standards and Technology for the"
        hdr["Comment"] = "FITS Definition document #100 and other FITS information"

        hdr["BZERO"] = 32768.0
        hdr["BSCALE"] = 1.0

        hdu = fits.PrimaryHDU(nda, header = hdr)
        #possible problem stems at file write
        img_file = f"{os.getenv('USERPROFILE')}/Desktop/test_9_6_1.fts"
        hdu.writeto(img_file, overwrite = True)
        print("IMAGE COLLECTED!")
        input("Press Enter for next exposure") #take out of final version, only here for testing
        
        
        





    #After image is taken tracking and connectivity should probably be == False I think...
    #user_validation_station()


#vroom vroom engine
running = True
while running == True:
    albert.Connected == True
    print(f"Telescope Connection Made: {albert.Connected}")
    print(f"Telescope Connection: {albert.Name}")
    print(f"Telescope Description: {albert.Description}")
    albert.Tracking = True
    print(f"Tracking On: {albert.Tracking}")
    print(f"Current Tracking Rate: {albert.TrackingRate}")
    print("""
    Tracking Rates Key:
    0 = Sidereal
    1 = Lunar
    2 = Solar
    3 = King 
    """)
    print(f"Tracking Rates Available: {albert.TrackingRates}")

    print("Beep Boop Bop Beep")
    print("Welcome To Telescope Controls")
    running = main_menu()