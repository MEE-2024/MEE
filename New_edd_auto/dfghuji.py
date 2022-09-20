import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import os

pathofdir = input("Please copy and paste the folder in which contains the fits files that you want stacked: ")
newpath = pathofdir.strip('"')


hdul = fits.open(newpath)
print(hdul.info())
hdr = hdul[0].header  # the primary HDU header
print(hdr)  # get the 2nd keyword's value
