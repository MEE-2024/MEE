import numpy as np

# Set up matplotlib
import matplotlib.pyplot as plt
from astropy.io import fits

imagedata = fits.getdata(r"C:\Users\kyleg\OneDrive\Desktop\test.fts")

print(type(imagedata))    #numpy.ndarray
print(imagedata.shape)    #(3520, 4656)


plt.imshow(imagedata, cmap='gray')
plt.colorbar()

plt.show()

   