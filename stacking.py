
import numpy as np
# Set up matplotlib
import matplotlib.pyplot as plt
from astropy.io import fits
import os
n = 0 
fitlist = []
pathofdir = 'fits files'
for filename in os.listdir(pathofdir):
    f = os.path.join(pathofdir, filename)
    fitlist.append(fits.getdata(f))

finalimage = np.sum(fitlist, axis = 0)
outfile = "fitsimage.fts"
hdu = fits.PrimaryHDU(finalimage)
hdu.writeto(outfile, overwrite = True)


imagedata = fits.getdata("fitsimage.fts")
plt.imshow(imagedata, cmap = 'gray', vmin = 2400, vmax = 2700)
plt.show()

    







   

