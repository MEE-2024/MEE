from alpaca.camera import *
from alpaca.telescope import *
from alpaca.exceptions import *
import socket

#This script strictly loads the camera into python
def camera_load():
    print("Please connect to your private network that you will be running ASCOM Alpaca.")
    input("Once completed, please press ENTER   ")

    hostname = socket.gethostname()
    IP_address = socket.gethostbyname(hostname)
    print(f"IP address of your private network:{IP_address}")
    port = 11111
    IP_port = IP_address + ":" + str(port)
    print(IP_port)

    try:
        global stacy
        stacy = Camera(IP_port, 0)
        stacy.Connected = True
        stacy.CoolerOn = True
        stacy.BinX = 1
        stacy.BinY = 1
        stacy.StartX = 0
        stacy.StartY = 0
        stacy.NumX = stacy.CameraXSize // stacy.BinX #int type
        stacy.NumY = stacy.CameraYSize // stacy.BinY
        print("Camera has successfully connected")
        input("Press enter to continue")
    except Exception as e:
        print(f"Exception occured: {str(e)}")
        quit()

    


    

    

    

