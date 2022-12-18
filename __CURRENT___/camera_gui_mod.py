from PySide6 import QtWidgets, QtCore, QtGui 
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QRadioButton, QTextBrowser
from PySide6.QtGui import QFont 
import time
import sys
import os
import numpy as np
import astropy.io.fits as fits
from alpaca.camera import *


bold_font = QFont("Arial",20, QFont.Bold)    #set font varibles so all text can be easily changed. 20 pt for titles
small_bold_font = QFont("Arial",12, QFont.Bold)   #12 pt for subtitles


class Camera_Func_Win(QMainWindow):
    def __init__(self):
        #parent constructor
        super(Camera_Func_Win,self).__init__()
        self.setWindowTitle("Camera Functions")
        self.cam_ip = self.get_cam_ip()

        #General commands needed
        self.stacy = Camera(f'{self.cam_ip}:11111',0)  #defines the camera
        self.stacy.CoolerOn = True   #turns on the cooler. Need try/except for this when using camera without fan
        
        #functions that are ran
        self.camera_on_off_func()   #needed to update camera state every 0.5 seconds. Issue: doesn't update state while taking images. 
        self.CAM_initUI()     #all GUI functions
        
        #temperature updater
        self.temp_update_timer = QTimer(self)   # creating a timer within the camera class
        self.temp_update_timer.setInterval(1000)  # 1 second timer
        self.temp_update_timer.timeout.connect(self.update_temp_label)  #when timer goes off, run update_temp_label
        self.temp_update_timer.start()  # Start the timer

        #camera state updater
        self.cam_state_update_timer = QTimer(self) #creates a timer for the camera state
        self.cam_state_update_timer.setInterval(500)  #.5 second timer
        self.cam_state_update_timer.timeout.connect(self.update_cam_state_label) #once timer goes off, runs update_cam_state_label
        self.cam_state_update_timer.start()   #starts the timer

        #terminal display
        self.text_browser = QTextBrowser(self)  #creates text browser
        self.text_browser.setGeometry(QtCore.QRect(900,350,600,400))
        self.text_browser.setStyleSheet("border: 5px solid black;""background-color : pink")
        self.text_browser.setFont(small_bold_font)  #did 12 pt font so you can see the text, but doesn't take up all the space
        sys.stdout = self  #ties python script output terminal to textbrowser
        sys.stderr = self  #ties python script exception outputs to the textbrowser



    #Function that writes to the QTextBrowser
    def write(self, text):
        self.text_browser.insertPlainText(text)  

    #Function that updates the temperature of the camera
    def update_temp_label(self):
        self.cam_temp_label.setText(f"Camera Temperature: {self.stacy.CCDTemperature} °C ")
        QApplication.processEvents()  #forces the QLabel to update

    #Function that updates the state of the camera
    def update_cam_state_label(self):
        if self.stacy.CameraState == 0:
            self.cam_state = '0 - Idle'
            self.cam_state_label.setText(f"Camera State: {self.cam_state} ")
            QApplication.processEvents()
        elif self.stacy.CameraState == 1:
            self.cam_state = '1 - Wait'
            self.cam_state_label.setText(f"Camera State: {self.cam_state} ")
            QApplication.processEvents()
        elif self.stacy.CameraState == 2:
            self.cam_state = '2 - Expose'
            self.cam_state_label.setText(f"Camera State: {self.cam_state} ")
            QApplication.processEvents()
        elif self.stacy.CameraState == 3:
            self.cam_state = '3 - Read'
            self.cam_state_label.setText(f"Camera State: {self.cam_state} ")
            QApplication.processEvents()
        elif self.stacy.CameraState == 4:
            self.cam_state = '4 - Download'
            self.cam_state_label.setText(f"Camera State: {self.cam_state} ")
            QApplication.processEvents()
        elif self.stacy.CameraState == 5:
            self.cam_state = '5 - Error'
            self.cam_state_label.setText(f"Camera State: {self.cam_state} ")
            QApplication.processEvents()
        else:
            print("Issue with assigning camera states")
       

    def CAM_initUI(self):

        #Camera state label
        self.cam_state_label = QtWidgets.QLabel(self)   #Label for camera state
        self.cam_state_label.setStyleSheet("border: 2px solid black;""background-color: cyan")
        self.cam_state_label.setText(f"Camera State: 0 - Idle ")  #Had to assign a string first, but is deleted after 0.5 seconds 
        self.cam_state_label.move(1100,200)   #position of label
        self.cam_state_label.setFont(bold_font)  #20 point bold arial font
        self.cam_state_label.adjustSize()    #automatically formats box to fit font size
        QApplication.processEvents()   #updates the changes since QLabels are Uneditable




        #Camera temp label
        self.cam_temp_label = QtWidgets.QLabel(self)
        self.cam_temp_label.setStyleSheet("border: 2px solid black;""background-color: cyan")
        self.cam_temp_label.move(1100,50)
        self.cam_temp_label.setText(f"Camera Temperature: {self.stacy.CCDTemperature} °C ") #seems redundent, but there must be some info in QLabel at the start
        self.cam_temp_label.setFont(bold_font)
        self.cam_temp_label.adjustSize()



        #Camera fan state label
        self.cam_fan_state_label = QtWidgets.QLabel(self)
        self.cam_fan_state_label.setStyleSheet("border: 2px solid black;""background-color: cyan")
        self.cam_fan_state_label.setText(f"Camera fan: {self.cam_fan} ")
        self.cam_fan_state_label.move(1100,125)
        self.cam_fan_state_label.setFont(bold_font)
        self.cam_fan_state_label.adjustSize()



        #Camera exposure amount label
        self.num_exposure_label = QtWidgets.QLabel(self)
        self.num_exposure_label.setStyleSheet("border: 2px solid black;""background-color: ")
        self.num_exposure_label.setText("Exposure Amount:")
        self.num_exposure_label.move(50,50)
        self.num_exposure_label.setFont(bold_font)
        self.num_exposure_label.adjustSize()

        #Camera exposure amount label value
        self.num_exposure_label_val = QtWidgets.QLabel(self)
        self.num_exposure_label_val.setGeometry(QtCore.QRect(50,100,260,50))  #(x,y,width, height)
        self.num_exposure_label_val.setStyleSheet("border: 2px solid black;""background-color: pink")
        self.num_exposure_label_val.setFont(bold_font)
        self.num_exposure_label_val.setAlignment(Qt.AlignCenter)
 
        #Cam exposure amount set value btn
        self.set_exp_amount_btn = QtWidgets.QPushButton(self)
        self.set_exp_amount_btn.setText("Set Number of Images")
        self.set_exp_amount_btn.clicked.connect(self.get_cam_exposure_amount)  #when clicked, sends to get_cam_exposure_amount
        self.set_exp_amount_btn.move(90,150)
        self.set_exp_amount_btn.setFont(small_bold_font)
        self.set_exp_amount_btn.adjustSize()



        #Cam exposure time label
        self.time_exposure_label = QtWidgets.QLabel(self)
        self.time_exposure_label.setStyleSheet("border: 2px solid black;""background-color: ")
        self.time_exposure_label.setText("Exposure Time:")
        self.time_exposure_label.move(350,50)
        self.time_exposure_label.setFont(bold_font)
        self.time_exposure_label.adjustSize()
        
        #Cam exposure time label value
        self.time_exposure_label_val = QtWidgets.QLabel(self)
        self.time_exposure_label_val.setGeometry(QtCore.QRect(352,100,220,50))  #(x,y,width, height)
        self.time_exposure_label_val.setStyleSheet("border: 2px solid black;""background-color: pink")
        self.time_exposure_label_val.setFont(bold_font)
        self.time_exposure_label_val.setAlignment(Qt.AlignCenter)
        
        #Cam exposure time set value btn
        self.time_exposure_btn = QtWidgets.QPushButton(self)
        self.time_exposure_btn.setText("Set Exposure Time")
        self.time_exposure_btn.clicked.connect(self.get_cam_exposure_time) 
        self.time_exposure_btn.move(385,150)
        self.time_exposure_btn.setFont(small_bold_font)
        self.time_exposure_btn.adjustSize()



        #Create file name label
        self.file_label = QtWidgets.QLabel(self)
        self.file_label.setStyleSheet("border: 2px solid black;""background-color: ")
        self.file_label.setText(" File Name: ")
        self.file_label.setFont(bold_font)
        self.file_label.move(50,250)
        self.file_label.adjustSize()
        
        #Create file name label value
        self.file_label_val = QtWidgets.QLabel(self)
        self.file_label_val.setStyleSheet("border: 2px solid black;""background-color: pink")
        self.file_label_val.setGeometry(QtCore.QRect(50,300,170,50))  #(x,y,width, height)
        self.file_label_val.setFont(bold_font)
        self.file_label_val.setAlignment(Qt.AlignCenter)  #center aligns any input
        
        #Create file name label value btn
        self.file_btn = QtWidgets.QPushButton(self)
        self.file_btn.setText("Set File Name")
        self.file_btn.clicked.connect(self.get_dir_file_name)
        self.file_btn.move(80,350)
        self.file_btn.setFont(small_bold_font)
        self.file_btn.adjustSize()



        #Create directory label
        self.dir_label = QtWidgets.QLabel(self)
        self.dir_label.setStyleSheet("border: 2px solid black;""background-color: ")
        self.dir_label.setText(" Directory Options: ")
        self.dir_label.setFont(bold_font)
        self.dir_label.move(260,250)
        self.dir_label.adjustSize()

        #create directory radio buttons
        self.main_dir = "C:"
        self.sec_dir = "D:"
        self.ter_dir = "E:"
        self.opt_dir = "Other:"

        #C drive radiobutton
        self.main_dir_radio = QRadioButton(self,"Mode Auto")
        self.main_dir_radio.setChecked(True)  #makes the button selected automatically, making it the default
        self.main_dir_radio.setText(self.main_dir)
        self.main_dir_radio.move(300,300)
        self.main_dir_radio.setFont(bold_font)
        self.main_dir_radio.clicked.connect(self.btn_state)

        #D drive radiobutton
        self.sec_dir_radio = QRadioButton(self,"Mode Auto")
        self.sec_dir_radio.setText(self.sec_dir)
        self.sec_dir_radio.move(300,330)    
        self.sec_dir_radio.setFont(bold_font)
        self.sec_dir_radio.clicked.connect(self.btn_state)
        
        #E drive radiobutton
        self.ter_dir_radio = QRadioButton(self,"Mode Auto")
        self.ter_dir_radio.setText(self.ter_dir)
        self.ter_dir_radio.move(300,360)
        self.ter_dir_radio.setFont(bold_font)
        self.ter_dir_radio.clicked.connect(self.btn_state)

        #Other radiobutton
        self.opt_dir_radio = QRadioButton(self,"Mode Auto")
        self.opt_dir_radio.setText(self.opt_dir)
        self.opt_dir_radio.move(300,390)
        self.opt_dir_radio.setFont(bold_font)
        self.opt_dir_radio.clicked.connect(self.btn_state)


        
        #Folderpath name display label
        self.folderpath_display_label = QtWidgets.QLabel(self)
        self.folderpath_display_label.setText(" Name of file path: ")
        self.folderpath_display_label.move(170,480)
        self.folderpath_display_label.setStyleSheet("border: 2px solid black;""background-color :")
        self.folderpath_display_label.setFont(bold_font)
        self.folderpath_display_label.adjustSize()

        #Folderpath name display value
        self.folderpath_display = QtWidgets.QLabel(self)
        self.folderpath_display.setStyleSheet("border: 2px solid black;""background-color: pink")
        self.folderpath_display.setGeometry(QtCore.QRect(50,530,500,50))  #(x,y,width, height)
        self.folderpath_display.setFont(small_bold_font)
        self.folderpath_display.setAlignment(Qt.AlignCenter)
       


        #Start Exposure Button
        self.start_exposure_btn = QtWidgets.QPushButton(self)
        self.start_exposure_btn.setText(" Start Exposure ")
        self.start_exposure_btn.setGeometry(175, 620, 250, 100)
        self.start_exposure_btn.setStyleSheet("border: 5px solid black;""background-color : lime")
        self.start_exposure_btn.setFont(bold_font)
        self.start_exposure_btn.clicked.connect(self.cam_exposure_func)



        #Create folder Button
        self.create_folder = QtWidgets.QPushButton(self)
        self.create_folder.setText(" Create Folder ")
        self.create_folder.setFont(small_bold_font)
        self.create_folder.move(250,580)
        self.create_folder.adjustSize()
        self.create_folder.clicked.connect(self.path_creater)



        #Terminal Display Label
        self.term_display_label = QtWidgets.QLabel(self)
        self.term_display_label.setText(" Terminal Output ")
        self.term_display_label.setStyleSheet("border: 2px solid black;""background-color : ")
        self.term_display_label.setFont(bold_font)
        self.term_display_label.move(1080,300)
        self.term_display_label.adjustSize()





    #gets ip address via user input
    def get_cam_ip(self):
        self.cam_user_ip_address_input, self.ok = QtWidgets.QInputDialog.getText(self, 'IP Address', 'Input IP Address:')
        if self.ok:   #if-statement allows the label to be placed if clicked Okay button
            self.cam_user_ip_address_label = QtWidgets.QLabel(self)
            self.cam_user_ip_address_label.setText(f"IP Address: {self.cam_user_ip_address_input}")#dont need [0] thing. Just does 1
            self.cam_user_ip_address_label.setStyleSheet("border: 2px solid black;""background-color: cyan")
            self.cam_user_ip_address_label.setFont(bold_font)
            self.cam_user_ip_address_label.move(650,50)
            self.cam_user_ip_address_label.adjustSize()
            return self.cam_user_ip_address_input   #needs to return the value or IP-adress is lost
        
        else:   #If you pressed cancel button or exit button, it exits the entire script
            print("exiting...")
            time.sleep(0.5)
            sys.exit()



    def camera_on_off_func(self):
        if self.stacy.CoolerOn == True:
            self.cam_fan = 'ON'
        elif self.stacy.CoolerOn == False:
            self.cam_fan = 'OFF'  
        else:
            print("Issue with camera_on_off_func")



    #creates file folder name and displays it in GUI
    def get_dir_file_name(self):
        self.dir_name, done1 = QtWidgets.QInputDialog.getText(self, "Name of File", 
        "Enter Name of Exposure File(s): ")
        print(f"File Root Name: {self.dir_name}")
        self.file_label_val.setText(self.dir_name)    
        print()
        print("get_dir_file_name function has been completed")
        print()

    #deals with button functions
    def btn_state(self):
        if self.main_dir_radio.isChecked() == True:
            print("main directory button is clicked")
            self.directory = self.main_dir
            return self.directory
           
        elif self.sec_dir_radio.isChecked()  == True:
            print("second directory button is clicked")
            self.directory = self.sec_dir
            return self.directory
            
        elif self.ter_dir_radio.isChecked()  == True:
            print("third directory button is clicked")
            self.directory = self.ter_dir
            return self.directory
            
        elif self.opt_dir_radio.isChecked() == True:
            print("other button is checked")
            self.other_directory()
        else:
            print("Issue with btn_state")



    #function to ask user to enter other directory input
    def other_directory(self):
        self.other_dir_name,self.okay = QtWidgets.QInputDialog.getText(self,"Other Directory",
         "Enter the name of the Other Directory")
        if self.okay:
            self.directory = self.other_dir_name
            self.opt_dir_radio.setText(self.directory)
            self.opt_dir_radio.adjustSize()
            QApplication.processEvents()
            return self.directory
        else:
            pass

    #function that creates the path in which the folder will be placed
    def path_creater(self):   #takes info on directory chosen and name of folder                               
        dir = os.path.join(self.directory, self.dir_name)  #joins the two paths of the main_dir and the file_name
        self.folderpath = os.path.abspath(dir) #folderpath is direct string of path(Ex: C:\user). Had to use dir, not self.dir cause os module can't use things of a class
        self.folderpath_display.setText(self.folderpath)  #displays the folderpath
        QApplication.processEvents()   #processes the change cause QLabels are uneditable
        print()
        print(self.folderpath)
        print()
        os.mkdir(self.folderpath)     #creates folderpath in designated directory
        


    #Display directory and filename in GUI to prevent loss in PC
    def cam_exposure_func(self):
        img_collected_count = 0 
        while img_collected_count != self.num_exposures:       #won't exit whileloop until img_collected_count == num_exps
            img_collected_count += 1                           #will add 1 after each iteration
            self.stacy.StartExposure(self.time_exposures, True)#starts exposure
            time_passed = 0
            while self.stacy.ImageReady == False:              #Will stay in whileloop until camera picture is ready. Due to Async.
                time.sleep(0.1)                                #Will check to see if ready every 0.1 second.
                time_passed += 0.1
                
            img = self.stacy.ImageArray                        #seting image as multidimensial array of pixel values
            imginfo = self.stacy.ImageArrayInfo
            imgDataType = np.uint64                            #KEEPS DATA AT 64 BITS OF INFO, NOT 16
            #add variable that looks for type of camera nad auto inputs it

            nda = np.array(img,dtype=imgDataType).transpose()     #converting array into FITS format
            hdr = fits.Header()                                   #tells variable that it will be the fits header
            hdr["Comment"] = "Fits (Flexible Image Transport System) format defined in Astronomy and"
            hdr["Comment"] = "Astrophysics Supplement Series v44/p363, v44/p371, v73/p359, v73/p365."
            hdr["Comment"] = "Contact the NASA Science Office of Standards and Technology for the"
            hdr["Comment"] = "FITS Definition document #100 and other FITS information"
            #add RA and DEC here. Will need to imported from mount function
            hdr["BZERO"] = 0                                #BZERO value for unit 16: 32768.0
            hdr["BSCALE"] = 1.0

            hdu = fits.PrimaryHDU(nda, header = hdr)            #converting data into fits file format
            #possible problem stems at file write
            name_var = f"{self.dir_name}_{img_collected_count}.fts"#name of fits file 
            print(f"name of file: {name_var}") 
            img_file = os.path.join(self.folderpath, name_var)    #Puts file in folder 
            img_file_path = os.path.abspath(img_file)             #write the absolute path into a variable
            hdu.writeto(img_file_path, overwrite = True)          #This overwrite = True could be a issue
            print(f"IMAGE {img_collected_count} COLLECTED!")
        print("Images have been successfully completed")
    
        
    
    def get_cam_exposure_time(self):
        #output of func to be used for exposure function
        #ask about maximum exposure time values
        self.time_exposures, done1 = QtWidgets.QInputDialog.getDouble(self, "Exposure Time", 
        "Enter Exposure Time: ",0,0.1,120.0,15)
        self.time_exposure_label_val.setNum(self.time_exposures)
        print(f"Exposure Time: {self.time_exposures}")
    


    #output of func to be used for exposure function
    def get_cam_exposure_amount(self):
        self.num_exposures, done1 = QtWidgets.QInputDialog.getInt(self, "Number of Exposures", 
        "Set Number of Exposures: ",0,0,100,0) #max exposures = 100
        self.num_exposure_label_val.setNum(self.num_exposures)
        print(f"Number of exposures: {self.num_exposures}")





#application start
def window():
    cam_app = QApplication(sys.argv)
    cam_win = Camera_Func_Win()
    #cam_win.show()
    cam_win.showMaximized()   #Automatically makes the window open on the entire screen
    sys.exit(cam_app.exec())  





if __name__ == "__main__":  
    window()