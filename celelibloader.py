import celelib


def libraryloader():

    diction = {}
    with open("Celestialibrary.txt", 'r') as library: #reads textfile in location
        for line in library: #forloop will iterate through each line in the library which is every dataset
            keyval = line.split(':') #split string from : to separate string key and string value
            diction[keyval[0]] = keyval[1] #assigns string key and value into dictionary key and value
        print()  
        keylist = sorted(diction.keys()) #organizes all keys into alphabetical order
        print(keylist)
        print()
        def inp():
            print("To copy and paste in terminal, use ctrl+shift+c/v.")
            a0 = input("Displayed above is a list of all celestial objects avaible. Copy and paste the celestial object you want to slew to: ")
            try:                    #try function was used instead of if statement that way if someone incorrectly spells a key,
                                    #it won't shut the complete program down, it will just prompt it to enter the except section
                a1 = diction[str(a0)]  #retreiving keyvalues from the inputed key
                a2 = a1.split(',') #separating RA and DEC tuple into separate variables
                a3 = a2[0] #Defining RA value as a variable string
                a4 = a2[1] #Defining DEC value as a varibale string
                a5 = a3.strip('(') #Deleting tuple format as string
                a6 = a4.strip(')\n') #Deleting rest of textfile format        
                global Ra
                Ra = float(a5) #Converting RA value into a float
                print("Right Ascension value:", Ra)
                global Dec #Converting DEC value into a float 
                Dec = float(a6)
                print("Declination value:", Dec)

            except:
                print("You didn't select a valid celestial object.")
                print("1 = add celestial object to library")
                print("2 = try again")
                a7 = input("Would you like to add this celestial object to the library or try again?>>>")
                if a7 == "1":
                    #was here
                    celelib.celestialibrary()
                elif a7 == "2":
                    inp()
                
                else:
                    inp()
            
            finally:
                pass
        inp()

#libraryloader()



        
            

        
        

