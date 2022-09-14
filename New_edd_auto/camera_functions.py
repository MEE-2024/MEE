import socket
import os
import time
import numpy as np
from alpaca.camera import *
from alpaca.telescope import *
from alpaca.exceptions import *
from camera import *
import astropy.io.fits as fits

camera_load()

print(f"Camera driver: {stacy.Name}")
print(f"Current Camera State: {stacy.CameraState}")
print(f"Sensor Name: {stacy.SensorName}, Sensor Type: {stacy.SensorType}")
print(f"Current CCD Temp: {stacy.CCDTemperature}")
print(f"Cooler is on: {stacy.CoolerOn}")
print(f"Current CCD Gain: {stacy.Gain}")
print(f"CCD Pixel Size: X = {stacy.PixelSizeX}, Y = {stacy.PixelSizeY}")
print(f"Max Camera ADU: {stacy.MaxADU}")

exp_time = float(input("Please input exposure time (float)(sec): "))
num_exps = int(input("Please Input the amount of continuous images you want taken: "))
file_name = str(input("Input file names (use _ for spaces): "))
setting = True
while setting == True:
    settings = input("Have you entered the camera settings yet? (y/n): ")
    if chr.lower(settings) == "y":
        from camera_settings import camera_state            #this is importing the camera_state variable set in settings. Might not work
        setting = False                                     #exits whileloop
    elif chr.lower(settings) == "n":
        camera_state = True                                 #default settings
        setting = False
    else:
        print("INPUT ERROR. ONLY POSSIBLE CHOICES ARE 'y' OR 'n'.")

#creating the directory of where images will be stored
DRIVE = True
while DRIVE == True:
    print("c = local hard drive")
    print("d = external hard drive")
    dir_choice = input("Do you want to save image files to the local hard drive or an external hard drive? >>>")
    if dir_choice.lower == "c":
        main_dir = "C:"
        DRIVE = False
    elif dir_choice.lower == "d":
        main_dir = "D:"
        DRIVE = False
    else:
        print("INPUT ERROR. THAT WAS NOT A CHOICE!")






dir = os.path.join(main_dir, file_name)             #joins the two paths of the main_dir and the file_name
os.mkdir(dir)                                       #makes folder in location
folderpath = os.path.abspath(dir)                   #folderpath is direct string of path(Ex: C:\user)






img_collected_count = 0                            
while img_collected_count != num_exps:                          #won't exit whileloop until img_collected_count == num_exps
    img_collected_count += 1                                    #will add 1 after each iteration
    stacy.StartExposure(exp_time, camera_state)                 #starts exposure
    time_passed = 0
    while stacy.ImageReady == False:                            #Will stay in whileloop until camera picture is ready. Due to Async.
        time.sleep(0.1)                                         #Will check to see if ready every 0.1 second.
        time_passed += 0.1
        if time_passed >= 120:                                   #this will break the camera process if it takes too long to take picture
            print("ERROR. Image is taking too long to be ready")
            print("Unable to capture image.")
            time.sleep(1)
            print("¯\_ (ツ)_/¯")
            img_collected_count = num_exps                      #this breaks out the primary whileloop
            break                                               #this breaks out of the innner whileloop
        else:
            pass                                                
    
        
    img = stacy.ImageArray                                #seting image as multidimensial array of pixel values
    imginfo = stacy.ImageArrayInfo
    imgDataType = np.uint64
    #add variable that looks for type of camera nad auto inputs it

    nda = np.array(img,dtype=imgDataType).transpose()     #converting array into numpy format
    hdr = fits.Header()
    hdr["Comment"] = "Fits (Flexible Image Transport System) format defined in Astronomy and"
    hdr["Comment"] = "Astrophysics Supplement Series v44/p363, v44/p371, v73/p359, v73/p365."
    hdr["Comment"] = "Contact the NASA Science Office of Standards and Technology for the"
    hdr["Comment"] = "FITS Definition document #100 and other FITS information"

    hdr["BZERO"] = 32768.0
    hdr["BSCALE"] = 1.0

    hdu = fits.PrimaryHDU(nda, header = hdr)              #converting data into fits file format
    #possible problem stems at file write
    name_var = f"{file_name}_{img_collected_count}.fts"   #name of fits file 
    print(f"name of file: {name_var}") 
    img_file = os.path.join(folderpath, name_var)         #Puts file in folder 
    img_file_path = os.path.abspath(img_file)             #write the absolute path into a variable
    hdu.writeto(img_file_path, overwrite = True)          #This overwrite = True could be a issue
    print(f"IMAGE {img_collected_count} COLLECTED!")


