import numpy as np

# Set up matplotlib
import matplotlib.pyplot as plt
from astropy.io import fits

with fits.open(r"C:\Users\kyleg\OneDrive\Desktop\test.fts") as hdulist:
    imagedata = hdulist[0].data
    header = hdulist[0].header
    #print(header)
    #print(data)
    print(hdulist.info())
    print(type(imagedata))    #numpy.ndarray
    print(imagedata.shape)    #(3520, 4656)


plt.imshow(imagedata, cmap='gray')
plt.colorbar()

plt.show()

   