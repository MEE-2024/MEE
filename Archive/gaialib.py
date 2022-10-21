import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord, Distance
from astropy.table import QTable

from astroquery.gaia import Gaia


hello = True

while hello:
    ans0 = input("Would you like to input celestial coordinate data? (y/n): ")
    if str.lower(ans0) == "y":
        Gaia.ROW_LIMIT = 10000  # Set the row limit for returned data
        name = input("Enter name of celestial object: ")
        try:
            cele = SkyCoord.from_name(name)
            global rA
            rA = cele.ra.hour
            global deC
            deC = cele.dec.deg
            print("Name of star:", name)
            print("Right Ascension value:", rA)
            print("Declination values:", deC)
            values = rA, deC 
            with open("Celestialibrary.txt", 'a') as library: #a is append, w is write, r is read
                    library.write('%s:%s\n' % (name, values)) 
            print("Celestial object successfully cataloged.")
        except:
            print("ERROR. Could not connect to GAIA database.")
            print("make sure you have a proper internet connection and/or proper spelling of celestial object.")

    elif str.lower(ans0) == "n":
        hello = False

    else:
        pass
print("Done!")


