
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import os


fitlist = []                                #creating list of fits files to stack
pathofdir = 'fits files'     #path of the directory
for filename in os.listdir(pathofdir):      
    f = os.path.join(pathofdir, filename)   #f is a new relative path of each file in the folder fits files
    fitlist.append(fits.getdata(f))         #storing each file in "fits files" folder in the list

finalimage = np.sum(fitlist, axis = 0)      #stacking fits files
outfile = "fitsimage.fts"    #outfile relative path
hdu = fits.PrimaryHDU(finalimage)           
hdu.writeto(outfile, overwrite = True)      #writing stacked fits files 

#This section allows us to see what the fits file looks like in python
imagedata = fits.getdata("fitsimage.fts")    
plt.imshow(imagedata, cmap = 'gray', vmin = 2400, vmax = 2700)  #the vmin and vmax were set based on the location of the center of the star
plt.show()                                                      #shows the image
#print(imagedata[4,4]) 
#maxval = np.max(imagedata)
#maxloc = np.where(imagedata = 65535, x, y)
#print(maxloc)  
             #remember that pixel coordinates(x,y) are in the form of (y,x) for numpy array

#image_hist = plt.hist(imagedata.flatten(), bins='auto')
#This is how I found the min and max of the image. 






   

