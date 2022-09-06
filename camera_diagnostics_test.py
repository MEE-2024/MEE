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

    input("Press Enter to Continue")

    stacy.StartExposure(1.0, True)
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
    input("Press Enter to Continue")
    
    


camera_test()
