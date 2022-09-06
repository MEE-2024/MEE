
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import os


fitlist = []                                #creating list of fits files to stack
pathofdir = 'Mount-Control\\fits files'     #path of the directory
for filename in os.listdir(pathofdir):      
    f = os.path.join(pathofdir, filename)   #f is a new relative path of each file in the folder fits files
    fitlist.append(fits.getdata(f))         #storing each file in "fits files" folder in the list

finalimage = np.sum(fitlist, axis = 0)      #stacking fits files
outfile = "Mount-Control\\fitsimage.fts"    #outfile relative path
hdu = fits.PrimaryHDU(finalimage)           
hdu.writeto(outfile, overwrite = True)      #writing stacked fits files 

#This section allows us to see what the fits file looks like in python
imagedata = fits.getdata("Mount-Control\\fitsimage.fts")    
plt.imshow(imagedata, cmap = 'gray', vmin = 2400, vmax = 2700)  #the vmin and vmax were set based on the location of the center of the star
plt.show()                                                      #shows the image

    







   

