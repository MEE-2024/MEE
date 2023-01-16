from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QTimer, Qt, QDateTime
from PySide6.QtWidgets import QApplication, QMainWindow, QTextBrowser, QSlider, QFileDialog
import matplotlib.pyplot as plt
from PySide6.QtGui import QFont 
import time as tme
import sys
import os
import numpy as np
import astropy.io.fits as fits
from astropy.time import Time
from alpaca.camera import *
from alpaca.telescope import *
import time



bold_font = QFont("Arial",15, QFont.Bold)    #set font varibles so all text can be easily changed. 20 pt for titles
small_bold_font = QFont("Arial",10, QFont.Bold)   #12 pt for subtitles
class Camera_Func_Win(QMainWindow):
    def __init__(self):
        #parent constructor
        super(Camera_Func_Win,self).__init__()
        self.setWindowTitle("Camera Functions for Reference Images")
        self.cam_ip = self.get_cam_ip()

        #General commands needed
        self.stacy = Camera(f'{self.cam_ip}:11111',0)  #defines the camera
        self.albert = Telescope(f'{self.cam_ip}:11111',0)



        
        self.stacy.CoolerOn = True   #turns on the cooler. Need try/except for this when using camera without fan
        self.stacy.BinX = 1                                          #standard BinX value (no binning cause 1)
        self.stacy.BinY = 1                                          #standard BinY values(no binning cause 1)
        self.stacy.StartX = 0                                        #Origin of pixel at (0,0)
        self.stacy.StartY = 0
        self.stacy.NumX = self.stacy.CameraXSize // self.stacy.BinX            #// = divide by and round to nearest integer
        self.stacy.NumY = self.stacy.CameraYSize // self.stacy.BinY
        self.RA = self.albert.RightAscension
        self.DEC = self.albert.Declination
        
        #functions that are ran
        self.camera_on_off_func()   #needed to update camera state every 0.5 seconds. Issue: doesn't update state while taking images.
        self.CAM_initUI()     #all GUI functions
        
        self.setStyleSheet("QInputDialog {background-color: pink;}")

        #temperature updater
        self.temp_update_timer = QTimer(self)   # creating a timer within the camera class
        self.temp_update_timer.setInterval(500)  # 0.5 second timer
        self.temp_update_timer.timeout.connect(self.update_temp_label)  #when timer goes off, run update_temp_label
        self.temp_update_timer.start()  # Start the timer

        #camera state updater
        self.cam_state_update_timer = QTimer(self) #creates a timer for the camera state
        self.cam_state_update_timer.setInterval(500)  #.5 second timer
        self.cam_state_update_timer.timeout.connect(self.update_cam_state_label) #once timer goes off, runs update_cam_state_label
        self.cam_state_update_timer.start()   #starts the timer

        #telescope location updater
        self.tele_loc_timer = QTimer(self) 
        self.tele_loc_timer.setInterval(500)
        self.tele_loc_timer.timeout.connect(self.update_tele_loc_label)
        self.tele_loc_timer.start()
        

        #terminal display
        self.text_browser = QTextBrowser(self)  #creates text browser
        self.text_browser.setGeometry(QtCore.QRect(650,350,600,280))
        self.text_browser.setStyleSheet("border: 5px solid black;""background-color : pink")
        self.text_browser.setFont(small_bold_font)  #did 12 pt font so you can see the text, but doesn't take up all the space
        sys.stdout = self  #ties python script output terminal to textbrowser
        sys.stderr = self  #ties python script exception outputs to the textbrowser



    #Function that writes to the QTextBrowser
    def write(self, text):
        self.text_browser.insertPlainText(text)   

    #Function that updates the temperature of the camera
    def update_temp_label(self):
        self.cam_temp_label.setText(f"Camera Temp: {self.stacy.CCDTemperature} °C ")
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

    def update_tele_loc_label(self):
        self.RA = self.albert.RightAscension
        self.DEC = self.albert.Declination
        self.round_ra = round(self.RA,2)
        self.round_dec = round(self.DEC,2)
        return self.RA, self.DEC, self.round_ra, self.round_dec
        
       
    def CAM_initUI(self):

        #Camera state label
        self.cam_state_label = QtWidgets.QLabel(self)   #Label for camera state
        self.cam_state_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.cam_state_label.setStyleSheet("background-color: cyan")
        self.cam_state_label.setText(f"Camera State: 0 - Idle ")  #Had to assign a string first, but is deleted after 0.5 seconds 
        self.cam_state_label.move(780,130)   #position of label
        self.cam_state_label.setFont(bold_font)  #20 point bold arial font
        self.cam_state_label.adjustSize()    #automatically formats box to fit font size
        QApplication.processEvents()   #updates the changes since QLabels are Uneditable
        
        #Camera temp label
        self.cam_temp_label = QtWidgets.QLabel(self)
        self.cam_temp_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.cam_temp_label.setStyleSheet("background-color: cyan")
        self.cam_temp_label.move(780,80)
        self.cam_temp_label.setText(f"Camera Temp: {self.stacy.CCDTemperature} °C ") #seems redundent, but there must be some info in QLabel at the start
        self.cam_temp_label.setFont(bold_font)
        self.cam_temp_label.adjustSize()



        #Camera fan state label
        self.cam_fan_state_label = QtWidgets.QLabel(self)
        self.cam_fan_state_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.cam_fan_state_label.setStyleSheet("background-color: cyan")
        self.cam_fan_state_label.setText(f"Camera fan: {self.cam_fan} ")
        self.cam_fan_state_label.move(780,180)
        self.cam_fan_state_label.setFont(bold_font)
        self.cam_fan_state_label.adjustSize()



        #Camera exposure amount label
        self.num_exposure_label = QtWidgets.QLabel(self)
        self.num_exposure_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.num_exposure_label.setStyleSheet("background-color: rgb(255,70,70) ")
        self.num_exposure_label.setText("Number of Exposures:")
        self.num_exposure_label.move(30,30)
        self.num_exposure_label.setFont(bold_font)
        self.num_exposure_label.adjustSize()

        #Camera exposure amount label value
        self.num_exposure_label_val = QtWidgets.QLabel(self)
        self.num_exposure_label_val.setGeometry(QtCore.QRect(30,70,225,40))  #(x,y,width, height)
        self.num_exposure_label_val.setStyleSheet("border: 2px solid black;""background-color: pink")
        self.num_exposure_label_val.setFont(bold_font)
        self.num_exposure_label_val.setAlignment(Qt.AlignCenter)
 
        #Cam exposure amount set value btn
        self.set_exp_amount_btn = QtWidgets.QPushButton(self)
        self.set_exp_amount_btn.setText("Set Number of Images")
        self.set_exp_amount_btn.setStyleSheet("background-color: rgb(211,211,211)")
        self.set_exp_amount_btn.clicked.connect(self.get_cam_exposure_amount)  #when clicked, sends to get_cam_exposure_amount
        self.set_exp_amount_btn.move(70,120)
        self.set_exp_amount_btn.setFont(small_bold_font)
        self.set_exp_amount_btn.adjustSize()



        #Cam exposure time label
        self.time_exposure_label = QtWidgets.QLabel(self)
        self.time_exposure_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.time_exposure_label.setStyleSheet("background-color:rgb(255,70,70) ")
        self.time_exposure_label.setText("Exposure Time [s]:")
        self.time_exposure_label.move(280,30)
        self.time_exposure_label.setFont(bold_font)
        self.time_exposure_label.adjustSize()
        
        #Cam exposure time label value
        self.time_exposure_label_val = QtWidgets.QLabel(self)
        self.time_exposure_label_val.setGeometry(QtCore.QRect(280,70,195,40))  #(x,y,width, height)
        self.time_exposure_label_val.setStyleSheet("border: 2px solid black;""background-color: pink")
        self.time_exposure_label_val.setFont(bold_font)
        self.time_exposure_label_val.setAlignment(Qt.AlignCenter)
        
        #Cam exposure time set value btn
        self.time_exposure_btn = QtWidgets.QPushButton(self)
        self.time_exposure_btn.setStyleSheet("background-color: rgb(211,211,211)")
        self.time_exposure_btn.setText("Set Exposure Time")
        self.time_exposure_btn.clicked.connect(self.get_cam_exposure_time) 
        self.time_exposure_btn.move(310,120)
        self.time_exposure_btn.setFont(small_bold_font)
        self.time_exposure_btn.adjustSize()



        #Create file name label
        self.file_label = QtWidgets.QLabel(self)
        self.file_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.file_label.setStyleSheet("background-color:rgb(255,70,70) ")
        self.file_label.setText(" File Name: ")
        self.file_label.setFont(bold_font)
        self.file_label.move(30,230)
        self.file_label.adjustSize()
        
        #Create file name label value
        self.file_label_val = QtWidgets.QLabel(self)
        self.file_label_val.setStyleSheet("border: 2px solid black;""background-color: pink")
        self.file_label_val.setGeometry(QtCore.QRect(30,270,125,40))  #(x,y,width, height)
        self.file_label_val.setFont(bold_font)
        self.file_label_val.setAlignment(Qt.AlignCenter)  #center aligns any input
        
        #Create file name label value btn
        self.file_btn = QtWidgets.QPushButton(self)
        self.file_btn.setText("Set File Name")
        self.file_btn.setStyleSheet("background-color: rgb(211,211,211)")
        self.file_btn.clicked.connect(self.get_dir_file_name)
        self.file_btn.move(45,320)
        self.file_btn.setFont(small_bold_font)
        self.file_btn.adjustSize()



        #Select Folder label
        self.folder_label = QtWidgets.QLabel(self)
        self.folder_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.folder_label.setStyleSheet("background-color: rgb(255,70,70)")
        self.folder_label.setText(" Folder Selection : ")
        self.folder_label.setFont(bold_font)
        self.folder_label.move(200,230)
        self.folder_label.adjustSize()

        #Select Folder label value
        self.folder_display = QtWidgets.QLabel(self)
        self.folder_display.setStyleSheet("border: 2px solid black;""background-color: pink")
        self.folder_display.setGeometry(QtCore.QRect(200,270,190,40))  #(x,y,width, height)
        self.folder_display.setFont(small_bold_font)
        self.folder_display.setAlignment(Qt.AlignCenter)



         #Select folder Button
        self.select_folder = QtWidgets.QPushButton(self)
        self.select_folder.setText(" Select Folder ")
        self.select_folder.setStyleSheet("background-color: rgb(211,211,211)")
        self.select_folder.setFont(small_bold_font)
        self.select_folder.move(250,320)
        self.select_folder.adjustSize()
        self.select_folder.clicked.connect(self.path_creater)
       


        #Start Exposure Button
        self.start_exposure_btn = QtWidgets.QPushButton(self)
        self.start_exposure_btn.setText(" Start Exposure ")
        self.start_exposure_btn.setGeometry(30, 525, 250, 100)
        self.start_exposure_btn.setStyleSheet("border: 5px solid black;""background-color : rgb(152,255,152)")
        self.start_exposure_btn.setFont(bold_font)
        self.start_exposure_btn.clicked.connect(self.cam_exposure_func)



        #Stop Exposure Button
        self.stop_exposure_btn = QtWidgets.QPushButton(self)
        self.stop_exposure_btn.setText(" Abort Exposure ")
        self.stop_exposure_btn.setGeometry(305,525,250,100)
        self.stop_exposure_btn.setStyleSheet("border: 5px solid black;""background-color :red")
        self.stop_exposure_btn.setFont(bold_font)
        self.stop_exposure_btn.clicked.connect(self.stacy.AbortExposure)



        #Stack/view Button
    


        #Terminal Display Label
        print("This is the terminal output")
        

         #Reference Star label
        self.ref_star =  QtWidgets.QLabel(self)
        self.ref_star.setText(" Name of Reference Stars: ")
        self.ref_star.setFont(bold_font)
        self.ref_star.move(500,30)
        self.ref_star.adjustSize()
        self.ref_star.setStyleSheet("background-color :rgb(255,70,70)")
        self.ref_star.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.ref_star.setAlignment(Qt.AlignCenter)

        #Reference Star value display
        self.ref_star_display = QTextBrowser(self)
        self.ref_star_display.setGeometry(QtCore.QRect(500,70,255,100))
        self.ref_star_display.setStyleSheet("border: 2px solid black;""background-color: pink")
        self.ref_star_display.setFont(small_bold_font)

        #Reference star button
        self.ref_star_btn = QtWidgets.QPushButton(self)
        self.ref_star_btn.setText('Input Star Reference')
        self.ref_star_btn.setFont(small_bold_font)
        self.ref_star_btn.move(560,180)
        self.ref_star_btn.adjustSize()
        self.ref_star_btn.setStyleSheet("background-color: rgb(211,211,211)")
        self.ref_star_btn.clicked.connect(self.ref_star_input)



        #Gain Label
        self.gain_label = QtWidgets.QLabel(self)
        self.gain_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.stacy.Gain = 30   #default
        self.gain_label.setText(f" Gain Values: {self.stacy.Gain}  ")
        self.gain_label.setStyleSheet("background-color :rgb(255,70,70) ")
        self.gain_label.setFont(bold_font)
        self.gain_label.move(680,230)
        self.gain_label.adjustSize()

        #Gain value slider
        self.gain_slider = QtWidgets.QSlider(self)
        self.gain_slider.setOrientation(Qt.Horizontal)
        self.gain_slider.setTickPosition(QSlider.TicksBelow)
        self.gain_slider.setTickInterval(10)
        self.gain_slider.setFixedWidth(240)
        self.gain_slider.setMinimum(0)
        self.gain_slider.setMaximum(100)
        self.gain_slider.setStyleSheet("background-color: pink ")
        self.gain_slider.move(650,280)
        self.gain_slider.valueChanged[int].connect(self.change_value)

        #0 tick label
        self.tick_0 = QtWidgets.QLabel(self)
        self.tick_0.setText('0')
        self.tick_0.setFont(small_bold_font)
        self.tick_0.move(651.5,305)

        #10 tick label
        self.tick_10 = QtWidgets.QLabel(self) 
        self.tick_10.setText('10')
        self.tick_10.setFont(small_bold_font)
        self.tick_10.move(669,305)

        #20 tick label
        self.tick_20 = QtWidgets.QLabel(self) 
        self.tick_20.setText('20')
        self.tick_20.setFont(small_bold_font)
        self.tick_20.move(693,305)

        #30 tick label
        self.tick_30 = QtWidgets.QLabel(self) 
        self.tick_30.setText('30')
        self.tick_30.setFont(small_bold_font)
        self.tick_30.move(716,305)

        #40 tick label
        self.tick_40 = QtWidgets.QLabel(self) 
        self.tick_40.setText('40')
        self.tick_40.setFont(small_bold_font)
        self.tick_40.move(739,305)

        #50 tick label
        self.tick_50 =  QtWidgets.QLabel(self) 
        self.tick_50.setText('50')
        self.tick_50.setFont(small_bold_font)
        self.tick_50.move(762,305)

        #60 tick label
        self.tick_60 = QtWidgets.QLabel(self) 
        self.tick_60.setText('60')
        self.tick_60.setFont(small_bold_font)
        self.tick_60.move(784,305)

        #70 tick label 
        self.tick_70 = QtWidgets.QLabel(self)
        self.tick_70.setText('70')
        self.tick_70.setFont(small_bold_font)
        self.tick_70.move(807,305)

        #80 tick label
        self.tick_80 = QtWidgets.QLabel(self)
        self.tick_80.setText('80')
        self.tick_80.setFont(small_bold_font)
        self.tick_80.move(830,305)

        #90 tick label
        self.tick_90 = QtWidgets.QLabel(self)
        self.tick_90.setText('90')
        self.tick_90.setFont(small_bold_font)
        self.tick_90.move(852,305)

        #100 tick label
        self.tick_100 = QtWidgets.QLabel(self)
        self.tick_100.setText('100')
        self.tick_100.setFont(small_bold_font)
        self.tick_100.move(875,305)

       

        #Focal Length Label
        self.focal_length_label = QtWidgets.QLabel(self)
        self.focal_length_label.setText(" Focal Length [m]: ")
        self.focal_length_label.setFont(bold_font)
        self.focal_length_label.setStyleSheet("background-color :rgb(255,70,70)")
        self.focal_length_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.focal_length_label.move(430,230)
        self.focal_length_label.adjustSize()

        #Focal Length label display
        self.focal_length_label_value = QtWidgets.QLabel(self)
        self.focal_length_label_value.setStyleSheet("border: 2px solid black;""background-color: pink")
        self.focal_length_label_value.setFont(small_bold_font)
        self.focal_length_label_value.setGeometry(QtCore.QRect(430,270,190,40))

        #Focal Length Button
        self.focal_length_btn = QtWidgets.QPushButton(self)
        self.focal_length_btn.setText("Set Focal Length")
        self.focal_length_btn.setStyleSheet("background-color: rgb(211,211,211)")
        self.focal_length_btn.move(470,320)
        self.focal_length_btn.setFont(small_bold_font)
        self.focal_length_btn.adjustSize()
        self.focal_length_btn.clicked.connect(self.get_focal_length)



        #Current RA label
        self.ra_label = QtWidgets.QLabel(self)
        self.update_tele_loc_label()
        self.ra_label.setText(f"RA [HH.hh]: {self.round_ra}")
        self.ra_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.ra_label.setGeometry(1050,30,200,23)
        self.ra_label.setFont(bold_font)
        self.ra_label.setStyleSheet("background-color: cyan")
        self.ra_label.setAlignment(Qt.AlignCenter)




        #Current DEC label
        self.dec_label = QtWidgets.QLabel(self)
        self.dec_label.setText(f"DEC [DD.dd]: {self.round_dec}")
        self.dec_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.dec_label.setGeometry(1050,80,200,23)
        self.dec_label.setFont(bold_font)
        self.dec_label.setStyleSheet("background-color: cyan")
        self.dec_label.setAlignment(Qt.AlignCenter)



        #Current Date Label
        self.date_label = QtWidgets.QLabel(self)
        self.date_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.date_label.setGeometry(1050,130,200,23)
        self.date_label.setFont(bold_font)
        self.date_label.setStyleSheet("background-color: cyan")
        self.date_label.setAlignment(Qt.AlignCenter)

        

        #Clock UTC Label
        self.UTC_time_label = QtWidgets.QLabel(self)
        self.UTC_time_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.UTC_time_label.setGeometry(1050,180,200,23)
        self.UTC_time_label.setFont(bold_font)
        self.UTC_time_label.setStyleSheet("background-color: cyan")
        self.UTC_time_label.setAlignment(Qt.AlignCenter)
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock_date)
        self.clock_timer.start(100)


        #ra label
        self.ra_label = QtWidgets.QLabel(self)
        self.ra_label.setText("Set RA [HH.hh]:")   #add units of HH:mm:ss. Want RA decimal to HH:mm:ss
        self.ra_label.move(920,230) 
        self.ra_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken) 
        self.ra_label.setStyleSheet("background-color: rgb(255,70,70)") 
        self.ra_label.setFont(bold_font)  
        self.ra_label.adjustSize()   #change font size, bolden, arial/comic sans, 12 point plus, also show more digits for number inputs

        #ra output label
        self.ra_output_label = QtWidgets.QLabel(self)                   
        self.ra_output_label.setStyleSheet("border: 2px solid black;""background-color: pink")
        self.ra_output_label.setFont(bold_font) 
        self.ra_output_label.setGeometry(QtCore.QRect(920,270,165,40))

        #ra button
        set_ra_Btn = QtWidgets.QPushButton(self)
        set_ra_Btn.setStyleSheet("background-color: lightgrey") 
        set_ra_Btn.setText("Set RA")
        set_ra_Btn.setFont(small_bold_font) 
        set_ra_Btn.adjustSize()
        set_ra_Btn.clicked.connect(self.take_ra_input)
        set_ra_Btn.move(965, 320)



        #dec label
        self.dec_label = QtWidgets.QLabel(self)
        self.dec_label.setText("Set DEC [DD.dd]:")   #add units of HH:mm:ss. Want RA decimal to HH:mm:ss
        self.dec_label.move(1110,230) 
        self.dec_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken) 
        self.dec_label.setStyleSheet("background-color: rgb(255,70,70)") 
        self.dec_label.setFont(bold_font)  
        self.dec_label.adjustSize()   #change font size, bolden, arial/comic sans, 12 point plus, also show more digits for number inputs

        #dec output label
        self.dec_output_label = QtWidgets.QLabel(self)                   
        self.dec_output_label.setStyleSheet("border: 2px solid black;""background-color: pink")
        self.dec_output_label.setFont(bold_font) 
        self.dec_output_label.setGeometry(QtCore.QRect(1110,270,170,40))

        #dec button
        set_dec_Btn = QtWidgets.QPushButton(self)
        set_dec_Btn.setStyleSheet("background-color: lightgrey") 
        set_dec_Btn.setText("Set DEC")
        set_dec_Btn.setFont(small_bold_font) 
        set_dec_Btn.adjustSize()
        set_dec_Btn.clicked.connect(self.take_dec_input)
        set_dec_Btn.move(1155, 320)



        #slew button
        slew_Btn = QtWidgets.QPushButton(self)
        slew_Btn.setText("Start Slew")
        slew_Btn.setFont(bold_font) 
        slew_Btn.clicked.connect(self.mount_movement_function)
        slew_Btn.setStyleSheet("border: 5px solid black;""background-color : rgb(152,255,152)")
        slew_Btn.setGeometry(30, 375, 250, 100)


        #Stop Movement label
        self.stop_move_label = QtWidgets.QPushButton(self)
        self.stop_move_label.setText("Abort Slew")
        self.stop_move_label.setGeometry(QtCore.QRect(305,375,250,100))
        self.stop_move_label.clicked.connect(self.abort_slew)
        self.stop_move_label.setStyleSheet("border: 5px solid black;""background-color :red")
        self.stop_move_label.setFont(bold_font) 
              


    #gets ip address via user input
    def get_cam_ip(self):
        print('get_cam_ip has been opened')
        self.cam_user_ip_address_input, self.ok = QtWidgets.QInputDialog.getText(self, 'IP Address', 'Input IP Address:')
        if self.ok:   #if-statement allows the label to be placed if clicked Okay button
            self.cam_user_ip_address_label = QtWidgets.QLabel(self)
            self.cam_user_ip_address_label.setText(f"IP Address: {self.cam_user_ip_address_input}")#dont need [0] thing. Just does 1
            self.cam_user_ip_address_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
            self.cam_user_ip_address_label.setStyleSheet("background-color: cyan")
            self.cam_user_ip_address_label.setFont(bold_font)
            self.cam_user_ip_address_label.move(780,30)
            self.cam_user_ip_address_label.adjustSize()
            return self.cam_user_ip_address_input   #needs to return the value or IP-adress is lost
        
        else:   #If you pressed cancel button or exit button, it exits the entire script
            print("exiting...")
            tme.sleep(0.5)
            sys.exit()

    def take_ra_input(self):
        #takes user ra input, updates label
        self.user_ra, done1 = QtWidgets.QInputDialog.getText(self, "Right Ascension Input", 
        "Enter Right Ascension: ")
        self.ra_output_label.setText(str(self.user_ra)) 
        print(self.user_ra)



    def take_dec_input(self):
        #takes user dec input, updates label
        self.user_dec, done1 = QtWidgets.QInputDialog.getText(self, "Declination Input", 
        "Enter Declination: ")
        self.dec_output_label.setText(str(self.user_dec))
        print(self.user_dec)


    def camera_on_off_func(self):
        if self.stacy.CoolerOn == True:
            self.cam_fan = 'ON'
        elif self.stacy.CoolerOn == False:
            self.cam_fan = 'OFF'  
        else:
            print("Issue with camera_on_off_func")

    def get_focal_length(self):
        self.focal_length_input, self.okkk = QtWidgets.QInputDialog.getDouble(self, 'Focal Length in Meters',
         'Input Focal Length in Meters:',0,0.1,10,4)
        if self.okkk:
            self.focal_length_label_value.setText(str(self.focal_length_input))
            return self.focal_length_input
        else:
            pass
    
    def abort_slew(self):
        self.albert.AbortSlew()

    def update_clock_date(self):
        # Get the current time in UTC
        self.now = QDateTime.currentDateTimeUtc()
        self.str_now = str(self.now)
        self.strip_time = self.str_now.replace('PySide6.QtCore.QDateTime','')
        self.strip_time_para_1 = self.strip_time.strip(')')
        self.strip_time_para_2 = self.strip_time_para_1.strip('(')
        self.strip_time_para_3 = self.strip_time_para_2.split(',')
        self.time_year = self.strip_time_para_3[0]
        self.time_month = self.strip_time_para_3[1]
        self.time_day = self.strip_time_para_3[2]
        self.time_hour = self.strip_time_para_3[3]
        self.time_minute = self.strip_time_para_3[4]
        self.time_seconds = self.strip_time_para_3[5]
        self.date_label.setText(f"Date: {self.time_month}/{self.time_day}/{self.time_year} ")
        self.UTC_time_label.setText(f"UTC: {self.time_hour}:{self.time_minute}:{self.time_seconds}")
       


    #creates file folder name and displays it in GUI
    def get_dir_file_name(self):
        print('get_dir_file_name has been opened')
        self.dir_name, done1 = QtWidgets.QInputDialog.getText(self, "Name of File", 
        "Enter Name of Exposure File(s): ")
        print(f"File Root Name: {self.dir_name}")
        self.file_label_val.setText(self.dir_name)    
        print()
        print("get_dir_file_name function has been completed")
        print()
        return self.dir_name



    #function that creates the path in which the folder will be placed
    def path_creater(self): 
        #function asks user to select disired folder containing fits images from GUI directory
        #and saves image selections directory for retrieval
        
        self.fit_img_folder_location = QFileDialog.getExistingDirectory()

        if self.fit_img_folder_location:
            # Print the selected file path
            print(self.fit_img_folder_location)
    
        else:
            print("Process canceled, no folder selected")
                                
        print('path_creater has been opened')
        self.dir = os.path.join(self.fit_img_folder_location, self.dir_name)  #joins the two paths of the main_dir and the file_name
        self.folderpath = os.path.abspath(self.fit_img_folder_location) #folderpath is direct string of path(Ex: C:\user). Had to use dir, not self.dir cause os module can't use things of a class
        self.folder_display.setText(self.folderpath)  #displays the folderpath
        QApplication.processEvents()   #processes the change cause QLabels are uneditable
        





    def stack_view(self):
        fitlist = []                                #creating list of fits files to stack                        #path of the directory
        for filename in os.listdir(self.dir):      
            f = os.path.join(self.dir, filename)   #f is a new relative path of each file in the folder fits files
            fitlist.append(fits.getdata(f))         #storing each file in "fits files" folder in the list

        finalimage = np.sum(fitlist, axis = 0)      #stacking fits files
        outfile = str(self.dir_name) + "_ref_stack.fts"              #outfile relative path 
        hdu = fits.PrimaryHDU(finalimage)           
        hdu.writeto(outfile, overwrite = True)      #writing stacked fits files 

        #This section allows us to see what the fits file looks like in python
        imagedata = fits.getdata(outfile)   
        plt.imshow(imagedata, cmap = 'gray')  
        plt.show()
                


    def ref_star_input(self):
        self.ref_star_display.clear()
        self.ref_num_stars, self.done19 = QtWidgets.QInputDialog.getInt(self, "Number of Reference Stars", 
        "Enter Number of Reference Stars: ",0,1,100,1)
        if self.done19:
            self.N = int(self.ref_num_stars)
            n = 1
            self.list_reference_star_names = []
            while self.N >= n:
                nameofref = "Enter Name of Reference Star" + str(n)
                self.ref_star_name, self.done20 = QtWidgets.QInputDialog.getText(self, "Name of Reference Star", 
                nameofref)
                if self.done20:
                    self.list_reference_star_names.append(self.ref_star_name)
                    self.ref_star_display.insertPlainText(self.ref_star_name)
                    self.ref_star_display.insertPlainText("\n")
                    n += 1
                else:
                    n = self.N + 1

            return self.N, self.list_reference_star_names

        else:
            pass
        
    def mount_movement_function(self):
        ra = float(self.user_ra)
        dec = float(self.user_dec)
        self.albert.SlewToCoordinatesAsync(RightAscension=ra,Declination=dec)
        while(self.albert.Slewing):
            time.sleep(1)
            print("Slewing...")

    def abort_slew(self):
        self.albert.AbortSlew
        print("Slew Aborted")



    #Display directory and filename in GUI to prevent loss in PC
    def cam_exposure_func(self):
        print('cam_exposure_func has been opened')
        img_collected_count = 0 
        while img_collected_count != self.num_exposures:       #won't exit whileloop until img_collected_count == num_exps
            img_collected_count += 1
            self.stacy.StartExposure(self.time_exposures, True)#starts exposure
            time_start = Time.now()

            while self.stacy.ImageReady == False:
                pass
                
            img = self.stacy.ImageArray                        #seting image as multidimensial array of pixel values
            imginfo = self.stacy.ImageArrayInfo
    
            #This will automatically assign the correct numpy formats and avoids writing BSCALE, BZERO, etc, to each one
            if imginfo.ImageElementType == 0:
                print('The image Array Type is Unknown')
                imgDataType = np.int16  #What to do with this?
                hdr = fits.Header()

            elif imginfo.ImageElementType == 1:
                print('The image Array Type is Int16')
                imgDataType = np.int16
                hdr = fits.Header()
                hdr['BZERO'] = int(0)
                hdr['BSCALE'] = int(1)


            elif imginfo.ImageElementType == 2: #Int32
                if self.stacy.MaxADU <= 65535:
                    imgDataType = np.uint16 # Required for BZERO & BSCALE to be written
                    print('The image Array Type is Uint16')
                    hdr = fits.Header()
                    hdr['BZERO'] = int(32768)  #2^15
                    hdr['BSCALE'] = int(1)
                else:
                    imgDataType = np.int32
                    print('THe image Array Type is int32')
                    hdr = fits.Header()
                    hdr['BZERO'] = 0
                    hdr['BSCALE'] = 1

            elif imginfo.ImageElementType == 3:
                print('The image Array Type is Double')
                imgDataType = np.double
                hdr = fits.Header()

            elif imginfo.ImageElementType == 4:
                print('The image Array Type is Single')
                imgDataType = np.single
                hdr = fits.Header()

            elif imginfo.ImageElementType == 5:
                print('The image Array Type is UInt64')
                imgDataType = np.uint64
                hdr = fits.Header()
                hdr['BZERO'] = int(2**63)
                hdr['BSCALE'] = int(0)

            elif imginfo.ImageElementType == 6:
                print('The image Array Type is Byte')
                imgDataType = np.byte
                hdr = fits.Header()

            elif imginfo.ImageElementType == 7:
                print('The image Array Type is Int64')
                imgDataType = np.int64
                hdr = fits.Header()
                hdr['BZERO'] = 0
                hdr['BSCALE'] = 1

            elif imginfo.ImageElementType == 8:
                print('The image Array Type is UInt16') 
                imgDataType = np.uint16
                hdr = fits.Header()
                hdr['BZERO'] = int(32768)  #2^15
                hdr['BSCALE'] = int(1)
           

            nda = np.array(img,dtype=imgDataType).transpose()     #converting array into FITS numpy and astropy format
            time_end = Time.now()



            
            hdr["CAMINFO"] = str(self.stacy.Description)
            hdr["GAIN"] = int(self.stacy.Gain)
            hdr["CCDTEMP"] = (float(self.stacy.CCDTemperature), 'Temperature of CCD camera in degrees Celsius')
            hdr["XBIN"] = int(self.stacy.BinX)
            hdr["YBIN"] = int(self.stacy.BinY)
            hdr["EXPTIME"] = (float(self.time_exposures), 'Exposure Time in seconds') 
            hdr["PIXELX"] = (float(self.stacy.PixelSizeX), 'Width of camera sensor elements in microns')
            hdr["PIXELY"] = (float(self.stacy.PixelSizeY), 'Height of camera sensor elements in microns')
            hdr["DATE-SRT"] = (str(time_start), 'Date of Image starting exposure in UTC') 
            hdr["DATE-END"] = (str(time_end), 'Date of image after exposure in UTC')
            hdr["RA"] = (float(self.RA), 'Right Ascension of the center of the image in decimal hours')
            hdr["DEC"] = (float(self.DEC), 'Declination of the center of the image in decimal degrees')
            hdr["FOCAL"] = (float(self.focal_length_input), 'Focal length of telescope used in meters')     
            hdr["Comment"] = "Fits (Flexible Image Transport System) format defined in Astronomy and"
            hdr["Comment"] = "Astrophysics Supplement Series v44/p363, v44/p371, v73/p359, v73/p365."
            hdr["Comment"] = "Contact the NASA Science Office of Standards and Technology for the"
            hdr["Comment"] = "FITS Definition document #100 and other FITS information"
            #There is no need to add BZERO and BSCALE values. It is automatically done with type of array, uint 64 
            #BZERO for uint 64 is 2^63, BZERO for uint 16 is 2^15
            #BSCALE is automatically set to 1

            hdu = fits.PrimaryHDU(nda, header = hdr)            #converting data into fits file format
            name_var = f"{self.dir_name}_{img_collected_count}_ref.fts"#name of fits file 
            print(f"name of file: {name_var}") 
            img_file = os.path.join(self.folderpath, name_var)    #Puts file in folder 
            img_file_path = os.path.abspath(img_file)             #write the absolute path into a variable
            hdu.writeto(img_file_path, overwrite = True)          #This overwrite = True could be a issue
            print(f"IMAGE {img_collected_count} COLLECTED!")
        
        print("Images have been successfully completed")





        ref_star_txt_file = os.path.join(self.folderpath,self.dir_name)
        with open(ref_star_txt_file, 'w') as ref_star_txt: #a is append, w is write, r is read
            for i in range(len(self.list_reference_star_names)):
                ref_star_txt.write(f'{self.list_reference_star_names[i]}\n')

                
    
        
    
    def get_cam_exposure_time(self):
        #output of func to be used for exposure function
        #ask about maximum exposure time values
        self.time_exposures, done1 = QtWidgets.QInputDialog.getDouble(self, "Exposure Time", 
        "Enter Exposure Time: ",0,0.1,120.0,8)
        self.time_exposure_label_val.setNum(self.time_exposures)
        print(f"Exposure Time: {self.time_exposures}")
    


    #output of func to be used for exposure function
    def get_cam_exposure_amount(self):
        self.num_exposures, done1 = QtWidgets.QInputDialog.getInt(self, "Number of Exposures", 
        "Set Number of Exposures: ",0,1,100,1) #max exposures = 100
        self.num_exposure_label_val.setNum(self.num_exposures)
        print(f"Number of exposures: {self.num_exposures}")



    def change_value(self):
        self.stacy.Gain = self.gain_slider.value()
        self.gain_label.setText(f" Gain Values: {self.stacy.Gain}  ")
        QApplication.processEvents()
        print(self.stacy.Gain)


#application start
def window():
    
    cam_app = QApplication(sys.argv)
    cam_app.setStyleSheet("QInputDialog {background-color: pink}")
    cam_win = Camera_Func_Win()
    print("###################   THIS IS THE TERMINAL OUTPUT   ###################")
    print()
    cam_win.setFixedSize(1280,650)
    cam_win.setStyleSheet("QMainWindow {background-color: rgb(255, 100, 100)}")
    cam_win.showMaximized()   #Automatically makes the window open on the entire screen
    sys.exit(cam_app.exec())  





if __name__ == "__main__":  
    window()