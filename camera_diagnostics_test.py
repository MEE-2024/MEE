import time
import os
import sys
import numpy as np

#Alpaca Library Imports
from alpaca.camera import *
from alpaca.telescope import *
from alpaca.exceptions import *

import astropy.io.fits as fits

stacy = Camera('192.168.1.47:11111',0)


def camera_test():
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
    print(f"Max Camera ADU: {stacy.MaxADU}")
    #still needs input validation
    imgs_collected = int(input("Please Input the amount of continuous images you want taken: "))
    img_exposure_time = float(input("Please input exposure time (float)(sec): "))
    #img_file_name = ""

    input("Press Enter to Begin Captures")
    img_collected_count = 0
    while img_collected_count != imgs_collected:
        img_collected_count += 1
        stacy.StartExposure(img_exposure_time, True)
        #while not stacy.ImageReady:
        time.sleep(img_exposure_time)
            #print(f"Image Ready: {stacy.ImageReady}")
            #print(f"Current Camera State: {stacy.CameraState}")
            #print(f"{stacy.PercentCompleted}")
        stacy.StopExposure() #I don't think that this is needed when stacy.imageready is being used, automatically swithes camera to idle after while loop exit

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
        name_var = f"test_{img_collected_count}.fts"
        print(f"name of file: {name_var}")
        input("Press Enter to continue")
        img_file = f"{os.getenv('USERPROFILE')}/Desktop/{name_var}"
        hdu.writeto(img_file, overwrite = True)
        print(f"IMAGE {img_collected_count} COLLECTED!")
        #input("Press Enter for next exposure") #take out of final version, only here for testing
    
    


camera_test()
