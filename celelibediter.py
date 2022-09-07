#The purpose of this file is to directly input new celestial objects into the textfile 


def celestialibrary():
    
    def namecele():
        global namecel
        namecel = input("Enter name of the celestial object: ")
        if len(namecel) == 0:
            print("Input Error. You did not enter any name.")
            namecele()
        else:
            pass

    def RAhrs():
        global RAhr
        RAhr = input("Enter RA hour: ")
        if len(RAhr) == 0:
            print("Input Error. You did not enter any data.")
            RAhrs()
        else:
            pass

    def RAmins():
        global RAmin
        RAmin = input("Enter RA minute: ")
        if len(RAmin) == 0:
            print("Input Error. You did not enter any data.")
            RAmins()
        else:
            pass

    def RAsecs():
        global RAsec
        RAsec = input("Enter RA second: ")
        if len(RAsec) == 0:
            print("Input Error. You did not enter any data.")
            RAsecs()
        else:
            pass

    def DECsign():
        global DECsigns
        DECsigns = input("Is the Declination positive or negative? (+/-): ")
        global s
        if DECsigns == '+':
            s = 1
        elif DECsigns == '-':
            s = -1
            print("Negative values have been accounted for. Next declination inputs, enter just its absolute value.")
        else:
            print("Error Input.")
            DECsign()

    def DECdegs():
        global DECdeg
        DECdeg = input("Enter DEC degree: ")
        if len(DECdeg) == 0:
            print("Input Error. You did not enter any data.")
            DECdegs()
        else:
            pass

    def DECmins():
        global DECmin
        DECmin = input("Enter DEC degree minute: ")
        if len(DECmin) == 0:
            print("Input Error. You did not enter any data.")
            DECmins()
        else:
            pass

    def DECsecs():
        global DECsec
        DECsec = input("Enter DEC degree second: ")
        if len(DECsec) == 0:
            print("Input Error. You did not enter any data.")
            DECsecs()
        else:
            pass

    #Input that controls whether to loop through or to stop
    def UIcel():
        global yn
        yn = input("Would you like to catalog another celestial object? (y/n): ")
        if str.lower(yn) == "y":
            celestialibrary()
                     
        elif str.lower(yn) == "n":
            pass
        else:
            print("Input Error. You did not choose any of the options.")
            UIcel()

    def RA():
        RAhrs()         #Input of RA hrs
        RAmins()        #Input of RA mins
        RAsecs() 

    def DEC():
        DECsign()       #Input of DEC signage
        DECdegs()       #Input of DEC hrs
        DECmins()       #Input of DEC mins
        DECsecs()

    def start():
        namecele()      #Input of celestial name.
        print()
        RA()
        print() 
        DEC()




    #This is where the program begins to run script
    print("#########################################################################")
    print("#####################\\\\\Celestial Dictionary UI/////#####################")
    print("#########################################################################")
    start()  #inputs of names, RA and DEC

    RAconv = abs(float(RAhr)) + (abs(float(RAmin))/60) + (abs(float(RAsec))/3600)  #Conversion to RA hrs
    if RAconv >= 24:
        print("Input error. The value of Right Ascension is too high.")  #upper bound of RA can't be 24 or higher
        RA()
    elif RAconv < 0:
        print("input Error. The value of Right Ascension is too low.") #lower bound of RA can't be less than 0
        RA()
    else:
        pass

    DECconv = s * (abs(float(DECdeg)) + (abs(float(DECmin))/60) + (float(DECsec))/3600) #Conversion to DEC hrs.

    if DECconv > 90:
        print("Input Error. The value of Declination is too high. ")  #upper bound of DEC can't be above 90
        DEC()
    elif DECconv < -90:
        print("Input Error. The value of Declination is too low. ") #lower bound of DEC can't be below 90
        DEC()
    else:
        pass


    values = RAconv, DECconv 
    with open("Celestialibrary_v_0_3.txt", 'a') as library: #a is append, w is write, r is read
                library.write('%s:%s\n' % (namecel, values)) 
    UIcel() #Prompts user to loop through or to add new data.   
    #print("Done.")

celestialibrary()

