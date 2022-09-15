from alpaca.camera import *
from alpaca.telescope import *
from alpaca.exceptions import *
import socket

def telescope_load():
    print("Please connect to your private network that you will be running ASCOM Alpaca.")
    input("Once completed, please press ENTER: ")

    hostname = socket.gethostname()                             #Finds IP address of the wireless network
    IP_address = socket.gethostbyname(hostname)
    print(f"IP address of your private network:{IP_address}")
    port = 11111                                                #default port number. Can be changed in ASCOM Remote server settings
    IP_port = IP_address + ":" + str(port)                      #Combines IP and port in format for Alpyca
    print(IP_port)


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
            albert.TrackingRate = DriveRates.driveLunar      #for some reason, on my end l in lunar must be capitalized
        else:
            print("ERROR. This was not a choice. Try again.")
            tracking_rates()



    try:
        global albert
        albert =  Telescope(IP_port, 0)
        albert.Connected = True
        tracking_rates()
        print(f"")
        print(f"Telescope mount connection state: {albert.Connected}")
        print(f"Telescope mount tracking state: {albert.Tracking}")
        print(f"Telescope mount tracking rate: {albert.TrackingRate}")
        print("Connection to telescope mount has been successful!")
        input("Press ENTER to continue: ")
        print()

    except Exception as e:
        print(f"Exception occured: {str(e)}")                   #Will print exception error from API
        quit() 


        

    




