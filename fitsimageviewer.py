import numpy as np

# Set up matplotlib
import matplotlib.pyplot as plt
from astropy.io import fits
path = input("Please paste the direct path of the chosen fits file to view: ")
newpath = path.strip('"')
imagedata = fits.getdata(newpath)

print(type(imagedata))    #numpy.ndarray
print(imagedata.shape)    #(3520, 4656)





image = plt.imshow(imagedata, cmap='gray')
plt.show()
plt.colorbar()



   