#Custom Imports
import celelib
import celelibloader

import time
import os
import sys
import numpy as np

#Alpaca Library Imports
from alpaca.camera import *
from alpaca.telescope import *
from alpaca.exceptions import *

import astropy.io.fits as fits
# random change caius did this

albert = Telescope('192.168.1.47:11111',0)
stacy = Camera('192.168.1.47:11111',0)
RA = albert.RightAscension
DEC = albert.Declination
stacy.Gain = 30
stacy.CoolerOn = True

def tracking_rates():
    print("""
    1 - star/planet
    2 - sun
    3 - moon
    """)
    track_rate = input("Select the desired object for your tracking rate: ")
    if track_rate == "1":
        albert.TrackingRate = DriveRates.driveSidereal
    elif track_rate == "2":
        albert.TrackingRate = DriveRates.driveSolar
    elif track_rate == "3":
        albert.TrackingRate = DriveRates.drivelunar
    else:
        print("ERROR. This was not a choice. Try again.")
        tracking_rates()

def camera_info():
        print(f"Current Camera State: {stacy.CameraState}")
        print(f"Sensor Name: {stacy.SensorName}, Sensor Type: {stacy.SensorType}")
        print(f"Current CCD Temp: {stacy.CCDTemperature}")
        print(f"Cooler is on: {stacy.CoolerOn}")
        print(f"Current CCD Gain: {stacy.Gain}")
        print(f"CCD Pixel Size: X = {stacy.PixelSizeX}, Y = {stacy.PixelSizeY}")
        print(f"Max Camera ADU: {stacy.MaxADU}")

def main_menu():
    #This function is the central hub for the user
    #Function finds out what type of input the user would like to input

    
    print("")
    print("""Make a Selection (int):
    1 - Slew to Position
    2 - Slew to Library Position
    3 - Slew to Home
    4 - Print Current DA/REC
    5 - Camera Control
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
    
    elif choice == "5":
        #send to validation station for passage to camera functions
        print(choice)
        user_validation_station(choice)

        
    elif choice.lower() == "x":
        print("Exiting Program")
        albert.Tracking = False
        albert.Connected = False
        print(f"Current mount RA: {RA}")
        print(f"Currnet mount DEC: {DEC}")
        running = False
        
        
    else:
        print("invalid input")
        print("INT TYPE INPUT ONLY")
        main_menu()

        
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
                deciding_location = False
            else:
                print("invalid response")

        #Send RA/DEC to mount control for slewing
        mount_movement_control(RA,DEC)
    
    elif user_choice == "2":
        print("Library of Coordinates")
        celelibloader.libraryloader()
        from celelibloader import Ra,Dec
        mount_movement_control(Ra, Dec)

    elif user_choice == "3":
        #this needs work
        #returns mount to 0/0
        #send RA and DEC to mount movement control
        print("choice 3")
        
        albert.SlewToCoordinatesAsync(RightAscension=0.0000000000, Declination=0.0000000000)
        print(f"RA = {albert.RightAscension}, DEC = {albert.Declination}")
        while(albert.Slewing):
            time.sleep(0.5)
            print("Doot... Doot... Doot...")

    elif user_choice == "5":
        greg = True
        #maybe nested while loops for exceptions
        
        exp_time = float(input("Please input exposure time (float)(sec): "))
        num_exps = int(input("Please Input the amount of continuous images you want taken: "))
        file_name = str(input("Input file names (use _ for spaces): "))
        
        main_dir = "D:"
        title = file_name                               #Places folder into external flashdrive. Could be issue for Linux or MAC
        dir = os.path.join(main_dir, title)            #create path using D:\ + "filename"
        os.mkdir(dir)      
        global folderpath                               #creates folder in dir path
        folderpath = os.path.abspath(dir)               #folderpath is the exact path    
########################################################################################################        
        camera_control(exp_time,num_exps,file_name)

    else:
        print("AGGGGGGHHHHH! HOW DID YOU GET HERE????")


def mount_movement_control(RA, DEC):
    print("You are at mount movement control")
    print(f"Current mount RA: {RA}")
    print(f"Currnet mount DEC: {DEC}")
    
    albert.SlewToCoordinatesAsync(RightAscension=RA, Declination=DEC)
    while(albert.Slewing):
        time.sleep(1)
        print(albert.RightAscension)
        print(albert.Declination)
        print("Doot... Doot... Doot...")
        
    print("Mount has been moved")
    print("returning to main menu...")
    time.sleep(1)
    main_menu()
        

def camera_control(exp_time,num_exps,file_name):
    """The purpose of this function is to control all camera functionality including exposure, 
    FITS image mapping, file naming and saving"""
    ##################################
    #Exposure Specification Variables#
    ##################################
    img_exposure_time = exp_time
    imgs_collected = num_exps
    img_file_name = file_name

    ###################
    #Camera Operations#
    ###################
    #stacy.Connected = True
    print(f"Camera Connection: {stacy.Connected}")
    stacy.BinX = 1
    stacy.BinY = 1
    #Assure full frame after binning change
    stacy.StartX = 0
    stacy.StartY = 0
    stacy.NumX = stacy.CameraXSize // stacy.BinX #int type
    stacy.NumY = stacy.CameraYSize // stacy.BinY
    
    camera_info()
    
    img_collected_count = 0                            #image count is 0 to start
    while img_collected_count != imgs_collected:       #while collected count does NOT equal image collected
        img_collected_count += 1  
        #true for night, false for day                     #Adds 1 to image count per iteration of while loop
        stacy.StartExposure(img_exposure_time, False)   #exposure for camera has started
        time_passed = 0
        while stacy.ImageReady == False:               #whileloop until exposure is done
            time.sleep(0.1)                            #will check to see if exposure is completed
            time_passed += 0.1
            if time_passed >= 60:
                print("ERROR. Image is taking too long to be ready")
                print("Unable to capture image.")
                time.sleep(2)
                print("¯\_ (ツ)_/¯")
                main_menu() 
            else:
                pass
        
        
        img = stacy.ImageArray                         #seting image as multidimensial array of pixel values
        imginfo = stacy.ImageArrayInfo
        imgDataType = np.uint64
        #add variable that looks for type of camera nad auto inputs it

        nda = np.array(img,dtype=imgDataType).transpose() #converting array into numpy format
        hdr = fits.Header()
        hdr["Comment"] = "Fits (Flexible Image Transport System) format defined in Astronomy and"
        hdr["Comment"] = "Astrophysics Supplement Series v44/p363, v44/p371, v73/p359, v73/p365."
        hdr["Comment"] = "Contact the NASA Science Office of Standards and Technology for the"
        hdr["Comment"] = "FITS Definition document #100 and other FITS information"

        hdr["BZERO"] = 32768.0
        hdr["BSCALE"] = 1.0

        hdu = fits.PrimaryHDU(nda, header = hdr)      #converting data into fits file format
        #possible problem stems at file write
        name_var = f"{img_file_name}_{img_collected_count}.fts"   #name of fits file
        print(f"name of file: {name_var}") 
        img_file = os.path.join(folderpath, name_var)
        img_file_path = os.path.abspath(img_file)
        hdu.writeto(img_file_path, overwrite = True)    #This overwrite = True could be a issue
        print(f"Curernt Camera Gain: {stacy.Gain}")
        print(f"IMAGE {img_collected_count} COLLECTED!")

    main_menu()


#vroom vroom engine

tracking_rates()
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
    running = main_menu()     #we did something here. If problem occurs, check here

