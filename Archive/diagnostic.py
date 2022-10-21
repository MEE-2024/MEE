import time
from alpaca.telescope import * # Multiple Classes including Enumerations
from alpaca.exceptions import * # Or just the exceptions you want to catch

def intro():
    T = Telescope('192.168.1.47:11111', 0) #Celestron telescope located in server freshtomato 50
   
    
    try:
        T.Connected = True
        print('Connected to', T.Name, '.')
        print(T.Description)
        print("Driver:", T.DriverInfo, "activated.")
        T.Tracking = True
        print("Telescope's current position in RA/DEC:", T.RightAscenson,T.Declination )


    except Exception as e: # Should catch specific
        InvalidOperationException
        print(f'Slew failed: {str(e)}')

    finally: # Assure that you disconnect
        T.FindHome
        print("Disconnecting...")
        T.Connected = False


