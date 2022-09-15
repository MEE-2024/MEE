from alpaca.camera import *
from alpaca.telescope import *
from alpaca.exceptions import *
import socket

#This script strictly loads the camera into python
def camera_load():
    print("Please connect to your private network that you will be running ASCOM Alpaca.")
    input("Once completed, please press ENTER: ")

    hostname = socket.gethostname()                             #Finds IP address of the wireless network
    IP_address = socket.gethostbyname(hostname)
    print(f"IP address of your private network:{IP_address}")
    port = 11111                                                #default port number. Can be changed in ASCOM Remote server settings
    IP_port = IP_address + ":" + str(port)                      #Combines IP and port in format for Alpyca
    print(IP_port)

    try:
        global stacy                                            #Stacy is global so can be used outside of module
        stacy = Camera(IP_port, 0)
        stacy.Connected = True                                  #Stacy is connected
        stacy.CoolerOn = True                                   #Cooling fan is on
        stacy.BinX = 1                                          #standard BinX value (no binning cause 1)
        stacy.BinY = 1                                          #standard BinY values(no binning cause 1)
        stacy.StartX = 0                                        #Origin of pixel at (0,0)
        stacy.StartY = 0
        stacy.NumX = stacy.CameraXSize // stacy.BinX            #// = divide by and round to nearest integer
        stacy.NumY = stacy.CameraYSize // stacy.BinY
        print("Camera has successfully connected")
        input("Press enter to continue")
        print()
    except Exception as e:
        print(f"Exception occured: {str(e)}")                   #Will print exception error from API
        quit()                                                  #Kills program
