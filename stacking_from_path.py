def stacking():

    import numpy as np
    import matplotlib.pyplot as plt
    from astropy.io import fits
    import os

    fitlist = []                                #creating list of fits files to stack
    pathofdir = input("Please copy and paste the folder in which contains the fits files that you want stacked: ")
    newpath = pathofdir.strip('"')
    title = input("Input the title of your stacked fits file: ")                             #path of the directory
    for filename in os.listdir(newpath):      
        f = os.path.join(newpath, filename)   #f is a new relative path of each file in the folder fits files
        fitlist.append(fits.getdata(f))         #storing each file in "fits files" folder in the list

    finalimage = np.sum(fitlist, axis = 0)      #stacking fits files
    outfile = str(title) + ".fts}"              #outfile relative path 
    hdu = fits.PrimaryHDU(finalimage)           
    hdu.writeto(outfile, overwrite = True)      #writing stacked fits files 

    #This section allows us to see what the fits file looks like in python
    imagedata = fits.getdata(outfile)   
    def response():
        ans1 = input("Would you like to see a picture of the stacked fits file? (y/n): ") 
        if str.lower(ans1) == "y":
            plt.imshow(imagedata, cmap = 'gray')  #the vmin and vmax were set based on the location of the center of the star
            plt.show()
        elif str.lower(ans1) == "n":
            pass
        else:
            print("INPUT ERROR")
            response()

    response()
    #possible ways to find pixel location of stars
    max = np.amax(imagedata)
    maxloc = np.where(imagedata  == max)
    print(f"Max pixel intensity value:{max}")
    print(f"Location of max pixel: {maxloc}")
    image_hist = plt.hist(imagedata.flatten(), bins='auto')  #use this to define vmin and vmax
    plt.show()




    #x = maxloc[0]
    #y = maxloc[1]
    #print(imagedata[x,y])
    
    #remember that pixel coordinates(x,y) are in the form of (y,x) for numpy array

stacking()