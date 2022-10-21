import socket
from alpaca.camera import *
from alpaca.telescope import *
from alpaca.exceptions import *
from camera import *
#This scripts allows the individual to change the camera settings. Right now only gain, but eventually all the data
#In future, GUI would have choices of cameras with all of their data stored in it. 
def camera_settings():

    camera_load()                                                                           #loads camera 
    yes = True
    while yes == True:
        raw_gain = input("Input gain integer value for camera: ")                           #try and except used to limit to integers
        try:                                                                                 
            gain = abs(int(raw_gain))
            yes = False
        except:
            print("INPUT ERROR. GAIN CANNOT BE STRING OR FLOAT")    

    print("daytime = 1")
    print("nighttime = 2")
    time_of_day = input("Will the camera be used in the daytime or the nighttime?>>> ")
    if time_of_day == "1":
        camera_state = False 
    elif time_of_day == "2":
        camera_state = True 
    from camera import stacy                                                               #import camera stacy from camera module
    stacy.Gain = gain
    print(f"Camera driver: {stacy.Name}")
    print(f"Current Camera State: {stacy.CameraState}")
    print(f"Sensor Name: {stacy.SensorName}, Sensor Type: {stacy.SensorType}")
    print(f"Current CCD Temp: {stacy.CCDTemperature}")
    print(f"Cooler is on: {stacy.CoolerOn}")
    print(f"Current CCD Gain: {stacy.Gain}")
    print(f"CCD Pixel Size: X = {stacy.PixelSizeX}, Y = {stacy.PixelSizeY}")
    print(f"Max Camera ADU: {stacy.MaxADU}")







