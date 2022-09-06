import numpy as np

# Set up matplotlib
import matplotlib.pyplot as plt
from astropy.io import fits

imagedata1 = fits.getdata(r"C:\Users\kyleg\OneDrive\Desktop\contents.fits")
imagedata2 = fits.getdata(r"C:\Users\kyleg\OneDrive\Desktop\contents1.fits")

#print(type(imagedata))    #numpy.ndarray
#print(imagedata.shape)    #(3520, 4656)





image1 = plt.imshow(imagedata1, cmap='gray')
plt.show()
image2 = plt.imshow(imagedata2, cmap = 'binary')
plt.show()
#plt.colorbar()

#plt.show()

   