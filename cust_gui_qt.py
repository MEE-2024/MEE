from ipaddress import ip_address
import string
from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow
import time
import sys
from alpaca.telescope import *

from matplotlib.pyplot import connect

#WIN FRAME CONSTANTS#

#where win shows up
XPOS = 450
YPOS = 100
#size of win
WIDTH = 500
HEIGHT = 500
#####################

class Mount_Movement_Win(QMainWindow):
    def __init__(self):
        #parent constructor
        super(Mount_Movement_Win,self).__init__()
        self.setGeometry(XPOS, YPOS, WIDTH, HEIGHT)
        self.setWindowTitle("Mount Movement Functions")
        self.initUI()  
    def initUI(self):
        #everything that goes inside the window goes inside this function

        #vars
        self.user_ra = 0.0
        self.user_dec = 0.0
        self.ra_max = 24.00000
        self.ra_min = 0.00000
        self.dec_max = 90.00000
        self.dec_min = -90.00000

        #ip input
        self.ip = self.get_tele_ip()
        self.albert = Telescope(f'{self.ip}:11111',0)

        #ra label
        self.ra_label = QtWidgets.QLabel(self)
        self.ra_label.setText("Desired Right Ascension:")
        self.ra_label.move(50,70)
        self.ra_label.adjustSize()

        #ra output label
        self.ra_output_label = QtWidgets.QLabel(self)
        self.ra_output_label.setStyleSheet("background-color: lightgrey")
        self.ra_output_label.move(50,95)

        #ra button
        set_ra_Btn = QtWidgets.QPushButton(self)
        set_ra_Btn.setText("Set RA")
        set_ra_Btn.clicked.connect(self.take_ra_input)
        set_ra_Btn.move(50, 130)

        #dec label
        self.dec_label = QtWidgets.QLabel(self)
        self.dec_label.setText("Desired Declination:")
        self.dec_label.move(50,170)
        self.dec_label.adjustSize()

        #dec output label
        self.dec_output_label = QtWidgets.QLabel(self)
        self.dec_output_label.setStyleSheet("background-color: lightgrey")
        self.dec_output_label.move(50,195)

        #dec button
        set_dec_Btn = QtWidgets.QPushButton(self)
        set_dec_Btn.setText("Set DEC")
        set_dec_Btn.clicked.connect(self.take_dec_input)
        set_dec_Btn.move(50, 230)

        #slew button
        slew_Btn = QtWidgets.QPushButton(self)
        slew_Btn.setText("Start Slew")
        slew_Btn.clicked.connect(self.mount_movement_function)
        slew_Btn.move(50, 270)

        #set tracking radio button
        self.track_rate_sidereal = QtWidgets.QRadioButton(self,"Mode Auto")
        self.track_rate_sidereal.setToolTip("Used for tracking stars and planets")
        self.track_rate_sidereal.toggled.connect(self.set_track_rate)
        self.track_rate_sidereal.mode = "Auto"
        self.track_rate_sidereal.move(305,95)
        self.sidereal_label = QtWidgets.QLabel(self)
        self.sidereal_label.setText("        Sidereal")
        self.sidereal_label.setStyleSheet("background-color: lightgrey")
        self.sidereal_label.move(330,95)

        #set track rate solar
        self.track_rate_solar = QtWidgets.QRadioButton(self,"Mode Auto")
        self.track_rate_solar.setToolTip("Used for tracking the Sun (SOL)")
        self.track_rate_solar.toggled.connect(self.set_track_rate)
        self.track_rate_solar.mode = "Auto"
        self.track_rate_solar.move(305,130)
        self.solar_label = QtWidgets.QLabel(self)
        self.solar_label.setText("        Solar")
        self.solar_label.setStyleSheet("background-color: lightgrey")
        self.solar_label.move(330,130)

        #set track rate lunar
        self.track_rate_lunar = QtWidgets.QRadioButton(self,"Mode Auto")
        self.track_rate_lunar.setToolTip("Used for tracking the moon (LUNAR)")
        self.track_rate_lunar.toggled.connect(self.set_track_rate)
        self.track_rate_lunar.mode = "Auto"
        self.track_rate_lunar.move(305,165)
        self.lunar_label = QtWidgets.QLabel(self)
        self.lunar_label.setText("        Lunar")
        self.lunar_label.setStyleSheet("background-color: lightgrey")
        self.lunar_label.move(330,165)

        #tracking rate main label
        self.tracking_list_label = QtWidgets.QLabel(self)
        self.tracking_list_label.setText("        Tracking Rates     ")
        self.tracking_list_label.setStyleSheet("background-color: lightgrey")
        self.tracking_list_label.move(305,70)
        self.tracking_list_label.adjustSize()

        #active slewing label
        self.active_ra_label = QtWidgets.QLabel(self)
        self.active_ra_label.setText("Current RA:")
        self.active_ra_label.move(100,350)

        #active ra label
        self.active_ra_slew_label = QtWidgets.QLabel(self)
        self.active_ra_slew_label.setStyleSheet("background-color: pink")
        self.active_ra_slew_label.move(250,350)

        #active dec label
        self.active_dec_label = QtWidgets.QLabel(self)
        self.active_dec_label.setText("Current DEC:")
        self.active_dec_label.move(100,450)

        #active dec slew label
        self.active_dec_slew_label = QtWidgets.QLabel(self)
        self.active_dec_slew_label.setStyleSheet("background-color: pink")
        self.active_dec_slew_label.move(250,450)
        #active slewing label
        self.active_slewing_label = QtWidgets.QLabel(self)
        self.active_slewing_label.setStyleSheet("background-color: lightgrey")
        self.active_slewing_label.setText("        Idle")
        self.active_slewing_label.move(330,20)


    #Functions
    def get_tele_ip(self):
        #self.albert = Telescope('192.168.1.21:11111',0)
        self.user_ip_address_input = QtWidgets.QInputDialog.getText(self, 'Input IP Address', 'IP Address:')
        self.ip_label = QtWidgets.QLabel(self)
        self.ip_label.setText(f"IP Address: {str(self.user_ip_address_input[0])}:11111")
        self.ip_label.setStyleSheet("background-color: pink")
        self.ip_label.move(50,20)
        self.ip_label.adjustSize()
        return self.user_ip_address_input[0]
    
    def take_ra_input(self):
        #takes user ra input, updates label
        self.user_ra, done1 = QtWidgets.QInputDialog.getDouble(self, "Input Dialog", 
        "Enter Right Ascension: ",0,self.ra_min,self.ra_max,15)
        self.ra_output_label.setText(str(self.user_ra))
        
        print(self.user_ra)

    def take_dec_input(self):
        #takes user dec input, updates label
        self.user_dec, done1 = QtWidgets.QInputDialog.getDouble(self, "Input Dialog", 
        "Enter Declination: ",0,self.dec_min,self.dec_max,15)
        self.dec_output_label.setText(str(self.user_dec))
        print(self.user_dec)

    def mount_movement_function(self):
        #moves mount, updates active slew label and slewing label
        ra = self.user_ra
        dec = self.user_dec
        
        self.albert.SlewToCoordinatesAsync(RightAscension=ra,Declination=dec)
        while(self.albert.Slewing):
            time.sleep(1)
            self.active_ra_slew_label.setText(self.albert.RightAscension)
            self.active_dec_slew_label.setText(self.albert.Declination)
            self.active_slewing_label.setStyleSheet("background-color: pink")
            self.active_slewing_label.setText("    Slewing")
            self.active_slewing_label.adjustSize()
        self.active_slewing_label.setStyleSheet("background-color: lightgrey")
        self.active_slewing_label.setText("        Idle")
        self.active_slewing_label.adjustSize()
        print(f"Mount has been moved to RA: {self.albert.RightAscension} DEC: {self.albert.Declination}")    
        
    def clicked(self):
        #updates widgets upon click
        self.ra_label.setText("You pressed the button")
        self.update()

    def update(self):
        #update given widget wrappers
        self.ra_label.adjustSize()
    
    def set_track_rate(self):
        #sets tracking rate dependent on which radiobutton is active, updates label color
        if self.track_rate_sidereal.isChecked() is True:
            self.sidereal_label.setStyleSheet("background-color: pink")
            print(self.track_rate_sidereal)
            print("Sidereal")
            self.albert.TrackingRate = DriveRates.driveSidereal
        else:
            self.sidereal_label.setStyleSheet("background-color: lightgrey")
            
        if self.track_rate_solar.isChecked() is True:
            self.solar_label.setStyleSheet("background-color: pink")
            print(self.track_rate_solar)
            print("Solar")
            self.albert.TrackingRate = DriveRates.driveSolar
        else:
            self.solar_label.setStyleSheet("background-color: lightgrey")

        if self.track_rate_lunar.isChecked() is True:
            self.lunar_label.setStyleSheet("background-color: pink")
            print(self.track_rate_lunar)
            print("Lunar")
            self.albert.TrackingRate = DriveRates.drivelunar

        else:
            self.lunar_label.setStyleSheet("background-color: lightgrey")



def start_slew_Btn():
    print("Start Slew Button has been clicked")


def window():
    app = QApplication(sys.argv)
    win = Mount_Movement_Win()
    win.show()
    #make sure that win shows nicely and exits on click "clean exit"
    sys.exit(app.exec())
window()