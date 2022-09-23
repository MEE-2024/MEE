from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow
import time
import sys
import os
import numpy as np
import astropy.io.fits as fits
from alpaca.camera import *
##############
#WIN POSITION
CAM_XPOS = 450
CAM_YPOS = 100
#SIZE OF WIN
CAM_WIDTH = 500
CAM_HEIGHT = 500
############## 192.168.1.21

#we need to make a day/night radio button



class Camera_Func_Win(QMainWindow):
    def __init__(self):
        #parent constructor
        super(Camera_Func_Win,self).__init__()
        self.setGeometry(CAM_XPOS, CAM_YPOS, CAM_WIDTH, CAM_HEIGHT)
        self.setWindowTitle("Camera Functions")
        self.CAM_initUI()
    def CAM_initUI(self):
        self.cam_ip = self.get_cam_ip()
        #commented out sections can be unblocked when running actual test
        self.stacy = Camera(f'{self.cam_ip}:11111',0)
        
        #GUI vars########################################################
        self.cam_state = self.stacy.CameraState#####maybe needs ()
        self.cam_temp = self.stacy.CCDTemperature
        self.cam_fan_on = self.stacy.CoolerOn
        self.exp_time_of_day = True
        #self.cam_state = "CAM TEST"
        #self.cam_temp = "TEMP TEST"
        #self.cam_fan_on_test = "ON TEST"
        #self.cam_fan_off_test = "OFF TEST 2"
        ################################################################

        #Cam exposure function vars################################
        #update comments when running real test

        #self.stacy.Connected = True                                  #Stacy is connected
        #self.stacy.BinX = 1                                          #standard BinX value (no binning cause 1)
        #self.stacy.BinY = 1                                          #standard BinY values(no binning cause 1)
        #self.stacy.StartX = 0                                        #Origin of pixel at (0,0)
        #self.stacy.StartY = 0
        #self.stacy.NumX = self.stacy.CameraXSize // self.stacy.BinX            #// = divide by and round to nearest integer
        #self.stacy.NumY = self.stacy.CameraYSize // self.stacy.BinY
        self.max_exposures = 100 #puts a limit on num exposure amounts
        self.exposure_time = 0.0 #for start exp duration float arg
        
        self.num_exposures = 0 #for img_collected_count for exposure while loop
        ###########################################################

        #IMG directory/file creation
        self.exposure_directory_name = ""

        ############################
        #Cam state label
        self.cam_state_label = QtWidgets.QLabel(self)
        self.cam_state_label.setStyleSheet("border: 1px solid black;""background-color: cyan")
        self.cam_state_label.setText("Camera State:")
        self.cam_state_label.move(50,50)
        self.cam_state_label.adjustSize()
        #Cam state label value
        self.cam_state_label_val = QtWidgets.QLabel(self)
        self.cam_state_label_val.setStyleSheet("border: 2px solid black;""background-color: pink")
        self.cam_state_label_val.setText(f"{self.cam_state}")
        self.cam_state_label_val.move(50,75)
        self.cam_state_label_val.adjustSize()

        #Cam temp label
        self.cam_temp_label = QtWidgets.QLabel(self)
        self.cam_temp_label.setStyleSheet("border: 1px solid black;""background-color: cyan")
        self.cam_temp_label.setText(f"Camera Temp:")
        self.cam_temp_label.move(200,50)#temp location
        self.cam_temp_label.adjustSize()
        #Cam temp label value
        self.cam_temp_label_val = QtWidgets.QLabel(self)
        self.cam_temp_label_val.setStyleSheet("border: 2px solid black;""background-color: pink")
        self.cam_temp_label_val.setText(f"{self.cam_temp}[C]")
        self.cam_temp_label_val.move(200,75)#temp location
        self.cam_temp_label_val.adjustSize()

        #Cam fan state label
        self.cam_fan_state_label = QtWidgets.QLabel(self)
        self.cam_fan_state_label.setStyleSheet("border: 1px solid black;""background-color: cyan")
        self.cam_fan_state_label.setText(f"Camera fan:")
        self.cam_fan_state_label.move(350,50)
        self.cam_fan_state_label.adjustSize()
        #Cam fan state label value
        self.cam_fan_state_label_val = QtWidgets.QLabel(self)
        self.cam_fan_state_label_val.setStyleSheet("border: 2px solid black;""background-color: pink")
        self.cam_fan_state_label_val.setText("FAN OFF")
        self.cam_fan_state_label_val.move(350,75)
        self.cam_fan_state_label_val.adjustSize()

        #Cam fan radiobutton on/off label
        self.cam_fan_on_label = QtWidgets.QLabel(self)
        self.cam_fan_on_label.setText("ON/OFF")
        self.cam_fan_on_label.setStyleSheet("border: 1px solid black;""background-color: cyan")
        self.cam_fan_on_label.move(350,100)
        self.cam_fan_on_label.adjustSize()
        #Cam fan radiobutton on/off value
        self.cam_fan_on = QtWidgets.QPushButton(self)
        self.cam_fan_on.setToolTip("Used to turn fan on")
        self.cam_fan_on.setChecked(False)
        self.cam_fan_on.toggled.connect(self.cam_fan_control)
        self.cam_fan_on.move(350,125)

        #Cam exposure amount label
        self.num_exposure_label = QtWidgets.QLabel(self)
        self.num_exposure_label.setStyleSheet("border: 1px solid black;""background-color: cyan")
        self.num_exposure_label.setText("Exposure Amount")
        self.num_exposure_label.move(50,200)
        self.num_exposure_label.adjustSize()
        #Cam exposure amount label value
        self.num_exposure_label_val = QtWidgets.QLabel(self)
        self.num_exposure_label_val.setStyleSheet("border: 2px solid black;""background-color: pink")
        self.num_exposure_label_val.move(51,225)
        #Cam exposure amount set value btn
        self.set_exp_amount_btn = QtWidgets.QPushButton(self)
        self.set_exp_amount_btn.setText("Set Exposure Amount")
        self.set_exp_amount_btn.clicked.connect(self.get_cam_exposure_amount)
        self.set_exp_amount_btn.move(50,260)
        self.set_exp_amount_btn.adjustSize()

        #Cam exposure time label
        self.time_exposure_label = QtWidgets.QLabel(self)
        self.time_exposure_label.setStyleSheet("border: 1px solid black;""background-color: cyan")
        self.time_exposure_label.setText("Exposure Time")
        self.time_exposure_label.move(200,200)
        self.time_exposure_label.adjustSize()
        #Cam exposure time label value
        self.time_exposure_label_val = QtWidgets.QLabel(self)
        self.time_exposure_label_val.setStyleSheet("border: 2px solid black;""background-color: pink")
        self.time_exposure_label_val.move(201,225)
        #Cam exposure time set value btn
        self.time_exposure_btn = QtWidgets.QPushButton(self)
        self.time_exposure_btn.setText("Set Exposure Time")
        self.time_exposure_btn.clicked.connect(self.get_cam_exposure_time)
        self.time_exposure_btn.move(200,260)
        self.time_exposure_btn.adjustSize()

        #Create dir/file name label
        self.create_dir_file_label = QtWidgets.QLabel(self)
        self.create_dir_file_label.setStyleSheet("border: 1px solid black;""background-color: cyan")
        self.create_dir_file_label.setText("Dir/File Name")
        self.create_dir_file_label.move(50,400)
        self.create_dir_file_label.adjustSize()
        #Create dir/file name label value
        self.create_dir_file_label_val = QtWidgets.QLabel(self)
        self.create_dir_file_label_val.setStyleSheet("border: 2px solid black;""background-color: pink")
        self.create_dir_file_label_val.move(51,425)
        #Create dir/file name label value btn
        self.create_dir_file_btn = QtWidgets.QPushButton(self)
        self.create_dir_file_btn.setText("Set Dir/File Name")
        self.create_dir_file_btn.clicked.connect(self.get_dir_file_name)
        self.create_dir_file_btn.move(50,460)
        self.create_dir_file_btn.adjustSize()

        #Cam day/night label
        self.cam_day_night_label = QtWidgets.QLabel(self)
        self.cam_day_night_label.setText("Day/Night")
        self.cam_day_night_label.setStyleSheet("border: 1px solid black;""background-color: cyan")
        self.cam_day_night_label.move(50,150)
        self.cam_day_night_label.adjustSize()
        #Cam day/night radiobutton set
        self.cam_day_night_btn = QtWidgets.QRadioButton(self,"Mode Auto")
        self.cam_day_night_btn.setToolTip("Sets cam day or night exposure. True = night, False = day")
        self.cam_day_night_btn.setChecked(True) #assumes photo taken at night
        self.cam_day_night_btn.toggled.connect(self.day_night_set)
        self.cam_day_night_btn.mode = "Auto"
        self.cam_day_night_btn.move(50,175)
    
    def day_night_set(self):
        if self.cam_day_night_btn.isChecked() == True:
            self.exp_time_of_day = True
            print("Cam setting = Night")
        else:
            self.exp_time_of_day = False
            print("Cam setting = Day")

    def cam_exposure_func(self):
        main_dir = "C:"                                     #Writes folder directory to local WINDOWS drive
        dir = os.path.join(main_dir, self.dir_name)             #joins the two paths of the main_dir and the file_name
        os.mkdir(dir)                                       #makes folder in location
        folderpath = os.path.abspath(dir)                   #folderpath is direct string of path(Ex: C:\user) 

        img_collected_count = 0 
        while img_collected_count != self.num_exposures:                          #won't exit whileloop until img_collected_count == num_exps
            img_collected_count += 1                                    #will add 1 after each iteration
            self.stacy.StartExposure(self.time_exposures, self.exp_time_of_day)                 #starts exposure
            time_passed = 0
            while self.stacy.ImageReady == False:                         #Will stay in whileloop until camera picture is ready. Due to Async.
                time.sleep(0.1)                                     #Will check to see if ready every 0.1 second.
                time_passed += 0.1
                if time_passed >= 120:                              #this will break the camera process if it takes too long to take picture
                    print("ERROR. Image is taking too long to be ready")
                    print("Unable to capture image.")
                    time.sleep(1)
                    print("¯\_ (ツ)_/¯")
                    img_collected_count = self.num_exposures

                else:
                    pass 
        img = self.stacy.ImageArray                                #seting image as multidimensial array of pixel values
        imginfo = self.stacy.ImageArrayInfo
        imgDataType = np.uint64                               #KEEPS DATA AT 64 BITS OF INFO, NOT 16
        #add variable that looks for type of camera nad auto inputs it

        nda = np.array(img,dtype=imgDataType).transpose()     #converting array into FITS format
        hdr = fits.Header()                                   #tells variable that it will be the fits header
        hdr["Comment"] = "Fits (Flexible Image Transport System) format defined in Astronomy and"
        hdr["Comment"] = "Astrophysics Supplement Series v44/p363, v44/p371, v73/p359, v73/p365."
        hdr["Comment"] = "Contact the NASA Science Office of Standards and Technology for the"
        hdr["Comment"] = "FITS Definition document #100 and other FITS information"

        hdr["BZERO"] = 0                                #BZERO value for unit 16: 32768.0
        hdr["BSCALE"] = 1.0

        hdu = fits.PrimaryHDU(nda, header = hdr)              #converting data into fits file format
        #possible problem stems at file write
        name_var = f"{self.dir_name}_{img_collected_count}.fts"   #name of fits file 
        print(f"name of file: {name_var}") 
        img_file = os.path.join(folderpath, name_var)         #Puts file in folder 
        img_file_path = os.path.abspath(img_file)             #write the absolute path into a variable
        hdu.writeto(img_file_path, overwrite = True)          #This overwrite = True could be a issue
        print(f"IMAGE {img_collected_count} COLLECTED!")

    print("Done")                    #this breaks out the primary whileloop

    def get_dir_file_name(self):

        #output of func to be used for exposure function
        #output of func to be used for dir creation function
        #ask about maximum exposure time values

        self.dir_name, done1 = QtWidgets.QInputDialog.getText(self, "Input Dialog", 
        "Enter Name of Exposure Dir/File(s): ")
        #self.time_exposure_label_val.setText(str(self.time_exposures))
        print(f"File Root Name: {self.dir_name}")
    
    def get_cam_exposure_time(self):

        #output of func to be used for exposure function
        #ask about maximum exposure time values

        self.time_exposures, done1 = QtWidgets.QInputDialog.getDouble(self, "Input Dialog", 
        "Enter Exposure Time: ",0,0.1,120.0,15)
        self.time_exposure_label_val.setText(str(self.time_exposures))
        print(f"Exposure Time: {self.time_exposures}")

    def get_cam_exposure_amount(self):

        #output of func to be used for exposure function

        self.num_exposures, done1 = QtWidgets.QInputDialog.getInt(self, "Input Dialog", 
        "Set Amount of Exposures: ",0,0,self.max_exposures,0)
        self.num_exposure_label_val.setText(str(self.num_exposures))
        print(f"Number of exposures: {self.num_exposures}")

    def get_cam_ip(self):

        #gets ip address via user input, displays label in top left of window

        self.cam_user_ip_address_input = QtWidgets.QInputDialog.getText(self, 'Input IP Address', 'IP Address:')
        self.cam_user_ip_address_label = QtWidgets.QLabel(self)
        self.cam_user_ip_address_label.setText(f"IP Address: {self.cam_user_ip_address_input[0]}:11111")
        self.cam_user_ip_address_label.setStyleSheet("border: 2px solid black;""background-color: pink")
        self.cam_user_ip_address_label.move(50,20)
        self.cam_user_ip_address_label.adjustSize()
        return self.cam_user_ip_address_input[0]
    def cam_fan_control(self):
        if self.cam_fan_on.isChecked() == True:

            #needs hardware testing and vars switched off from test vars

            self.stacy.CoolerOn = True
            print(self.stacy.CoolerOn)
            self.cam_fan_state_label_val.setText(f"{self.cam_fan_on}")
            self.cam_fan_state_label_val.adjustSize() #always use adjust size at label changes
            print("cooler on")
        else:
            self.stacy.CoolerOn = False
            print(self.stacy.CoolerOn)
            self.cam_fan_state_label_val.setText(f"{self.cam_fan_on}")
            self.cam_fan_state_label_val.adjustSize()
            print("cooler off")



#application start
def window():
    cam_app = QApplication(sys.argv)
    cam_win = Camera_Func_Win()
    cam_win.show()
    #make sure that win shows nicely and exits on click "clean exit"
    sys.exit(cam_app.exec())
window()