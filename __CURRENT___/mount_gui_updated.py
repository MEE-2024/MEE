from PySide6 import QtWidgets 
import PySide6.QtGui as QtGui
from PySide6.QtGui import QFont,Qt
from PySide6.QtWidgets import QWidget,QTextBrowser, QRadioButton
from PySide6.QtWidgets import QApplication  #, QMainWindow
import PySide6.QtCore as QtCore
from PySide6.QtCore import QTimer,QDateTime
import time
import sys
from alpaca.telescope import *


class Mount_Movement_Win(QWidget):
    def __init__(self):
        #parent constructor
        super(Mount_Movement_Win,self).__init__()

        self.initUI() 

        #timer for mount state
        self.mount_state_update_timer = QTimer(self) #creates a timer for the camera state
        self.mount_state_update_timer.setInterval(500)  #.5 second timer
        self.mount_state_update_timer.timeout.connect(self.update_mount_state_label) #once timer goes off, runs update_cam_state_label
        self.mount_state_update_timer.start()   #starts the timer
        self.setWindowTitle("Mount Movement Functions")

        #timer for current RA and DEC
        self.loc_timer = QTimer(self) 
        self.loc_timer.setInterval(500)
        self.loc_timer.timeout.connect(self.update_loc_label)
        self.loc_timer.start()

        #output terminal
        self.text_browser = QTextBrowser(self) #creates text browser 
        self.text_browser.setGeometry(QtCore.QRect(750,250,600,400)) 
        self.text_browser.setStyleSheet("border: 5px solid black;""background-color : pink") 
        self.text_browser.setFont(self.small_bold_font) #did 12 pt font so you can see the text, but doesn't take up all the space sys.stdout = self #ties python script output terminal to textbrowser 
        sys.stdout = self
        sys.stderr = self #ties python script exception outputs to the textbrowser 
#######################################################################################################    
#######################################################################################################      
#######################################################################################################
#######################################################################################################
#######################################################################################################     
    #writes output and error messages to TextBrowser
    def write(self, text): 
        self.text_browser.insertPlainText(text) 



    #controls the mount state
    def update_mount_state_label(self):   
        if self.albert.Slewing is True:
            self.active_slewing_label.setText(f"Mount State: {self.albert.Slewing}")
            self.active_slewing_label.setStyleSheet("background-color: red")
            QApplication.processEvents()
        elif self.albert.Slewing is False:
            self.active_slewing_label.setText(f"Mount State: {self.albert.Slewing}")
            self.active_slewing_label.setStyleSheet("background-color: cyan")
            QApplication.processEvents()
        else:
            print('issue involving update_mount_state_label')



    #update the current DEC and RA of mount
    def update_loc_label(self):
        self.RA = self.albert.RightAscension
        self.DEC = self.albert.Declination
        self.active_ra_slew_label.setText(str(self.RA))
        self.active_dec_slew_label.setText(str(self.DEC))
        QApplication.processEvents()
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
#######################################################################################################
    #defines all GUI visual reps
    def initUI(self):
        #initial variables
        self.user_ra = 0.0
        self.user_dec = 0.0
        self.ra_max = 24.00000
        self.ra_min = 0.00000
        self.dec_max = 90.00000
        self.dec_min = -90.00000

        

        #fonts
        self.bold_font = QFont("Arial",20, QFont.Bold) #set font varibles so all text can be easily changed. 20 pt for titles 
        self.small_bold_font = QFont("Arial",12, QFont.Bold) #12 pt for subtitles 
        


        #ip input
        self.ip = self.get_tele_ip()
        self.albert = Telescope(f'{self.ip}:11111',0)
        


        #active slewing label
        self.active_slewing_label = QtWidgets.QLabel(self)
        self.active_slewing_label.setStyleSheet("background-color: lightgrey")
        self.active_slewing_label.setFont(self.bold_font)
        self.active_slewing_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.active_slewing_label.setStyleSheet("background-color: pink")
        self.active_slewing_label.setGeometry(1050,50,290,33)



        #Clock UTC label
        self.utc_clock_label = QtWidgets.QLabel(self)
        self.utc_clock_label.setGeometry(1050,100,290,33)
        self.utc_clock_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.utc_clock_label.setStyleSheet("background-color: pink")
        self.utc_clock_label.setFont(self.bold_font)
        self.utc_clock_label.setAlignment(Qt.AlignCenter) 
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)



        #current date label
        self.date_label = QtWidgets.QLabel(self)
        self.date_label.setGeometry(700,100,290,33)
        self.date_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.date_label.setStyleSheet("background-color: pink")
        self.date_label.setFont(self.bold_font)
        self.date_label.setAlignment(Qt.AlignCenter) 



        #terminal label
        self.terminal_label = QtWidgets.QLabel(self)
        self.terminal_label.setStyleSheet("background-color: lightgrey")
        self.terminal_label.setText("Terminal Output")
        self.terminal_label.setFont(self.bold_font)
        self.terminal_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.terminal_label.setAlignment(Qt.AlignCenter)
        self.terminal_label.setStyleSheet("background-color: pink")
        self.terminal_label.setGeometry(940,200,225,33)



        #ra label
        self.ra_label = QtWidgets.QLabel(self)
        self.ra_label.setText("Right Ascension:")   #add units of HH:mm:ss. Want RA decimal to HH:mm:ss
        self.ra_label.move(50,50) 
        self.ra_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken) 
        self.ra_label.setStyleSheet("background-color: rgb(255,70,70)") 
        self.ra_label.setFont(self.bold_font)  
        self.ra_label.adjustSize()   #change font size, bolden, arial/comic sans, 12 point plus, also show more digits for number inputs

        #ra output label
        self.ra_output_label = QtWidgets.QLabel(self)                   
        self.ra_output_label.setStyleSheet("background-color: pink") 
        self.ra_output_label.setFont(self.bold_font) 
        self.ra_output_label.setGeometry(QtCore.QRect(50,95,237,50))

        #ra button
        set_ra_Btn = QtWidgets.QPushButton(self)
        set_ra_Btn.setStyleSheet("background-color: lightgrey") 
        set_ra_Btn.setText("Set RA")
        set_ra_Btn.clicked.connect(self.take_ra_input)
        set_ra_Btn.move(125, 150)
         


        #dec label
        self.dec_label = QtWidgets.QLabel(self)
        self.dec_label.setText("Declination:")   #add units of HH:mm:ss. Want RA decimal to HH:mm:ss
        self.dec_label.move(50,215) 
        self.dec_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken) 
        self.dec_label.setStyleSheet("background-color: rgb(255,70,70)") 
        self.dec_label.setFont(self.bold_font)  
        self.dec_label.adjustSize() 

        #dec output label
        self.dec_output_label = QtWidgets.QLabel(self)                   
        self.dec_output_label.setStyleSheet("background-color: pink") 
        self.dec_output_label.setFont(self.bold_font) 
        self.dec_output_label.setGeometry(QtCore.QRect(50,260,237,50))

        #dec button
        set_dec_Btn = QtWidgets.QPushButton(self)
        set_dec_Btn.setText("Set DEC")
        set_dec_Btn.setStyleSheet("background-color: lightgrey") 
        set_dec_Btn.clicked.connect(self.take_dec_input)
        set_dec_Btn.move(125, 315)



        #slew button
        slew_Btn = QtWidgets.QPushButton(self)
        slew_Btn.setText("Start Slew")
        slew_Btn.setFont(self.bold_font) 
        slew_Btn.clicked.connect(self.mount_movement_function)
        slew_Btn.setStyleSheet("background-color: rgb(152,255,152)")
        slew_Btn.setGeometry(QtCore.QRect(50,520,150,50))



        #Stop Movement label
        self.stop_move_label = QtWidgets.QPushButton(self)
        self.stop_move_label.setText("Abort Slew")
        self.stop_move_label.setGeometry(QtCore.QRect(220,520,150,50))
        self.stop_move_label.clicked.connect(self.abort_slew)
        self.stop_move_label.setStyleSheet("background-color: rgb(204,2,2)")
        self.stop_move_label.setFont(self.bold_font) 



        #active slewing label
        self.active_ra_label = QtWidgets.QLabel(self)
        self.active_ra_label.setText("Current RA:")   
        self.active_ra_label.move(250,400) 
        self.active_ra_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken) 
        self.active_ra_label.setStyleSheet("background-color: rgb(255,70,70)") 
        self.active_ra_label.setFont(self.bold_font)  
        self.active_ra_label.adjustSize()

        #active ra label
        self.active_ra_slew_label = QtWidgets.QLabel(self)
        self.active_ra_slew_label.setStyleSheet("background-color: pink")
        self.active_ra_slew_label.setGeometry(QtCore.QRect(450,400,237,32))
        self.active_ra_slew_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)

        #active dec label
        self.active_dec_label = QtWidgets.QLabel(self)
        self.active_dec_label.setText("Current DEC:")   
        self.active_dec_label.move(250,450) 
        self.active_dec_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken) 
        self.active_dec_label.setStyleSheet("background-color: rgb(255,70,70)") 
        self.active_dec_label.setFont(self.bold_font)  
        self.active_dec_label.adjustSize()

        #active dec slew label
        self.active_dec_slew_label = QtWidgets.QLabel(self)
        self.active_dec_slew_label.setStyleSheet("background-color: pink")
        self.active_dec_slew_label.setGeometry(QtCore.QRect(450,450,237,32))
        self.active_dec_slew_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)



        #tracking rates label
        self.tracking_rate = QtWidgets.QLabel(self)
        self.tracking_rate.setText(" Tracking Rates: ")
        self.tracking_rate.setStyleSheet("background-color: rgb(255,70,70)")
        self.tracking_rate.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.tracking_rate.setFont(self.bold_font)
        self.tracking_rate.adjustSize()
        self.tracking_rate.move(370,50)

         #Tracking Rates radio buttons
        self.tracking_sidereal = "Sidereal"
        self.tracking_solar = "Solar"
        self.tracking_lunar = "Lunar"
       
        #Sidereal radiobutton
        self.tracking_sidereal_radio = QRadioButton(self,"Mode Auto")
        #self.tracking_sidereal_radio.setChecked(True)  #makes the button selected automatically, making it the default
        self.tracking_sidereal_radio.setText(self.tracking_sidereal)
        self.tracking_sidereal_radio.move(370,100)
        self.tracking_sidereal_radio.setFont(self.bold_font)
        self.tracking_sidereal_radio.clicked.connect(self.tracking_btn_state)

        #Solar radiobutton
        self.tracking_solar_radio = QRadioButton(self,"Mode Auto")
        self.tracking_solar_radio.setText(self.tracking_solar)
        self.tracking_solar_radio.move(370,130)    
        self.tracking_solar_radio.setFont(self.bold_font)
        self.tracking_solar_radio.clicked.connect(self.tracking_btn_state)
        
        #Lunar radiobutton
        self.tracking_lunar_radio = QRadioButton(self,"Mode Auto")
        self.tracking_lunar_radio.setText(self.tracking_lunar)
        self.tracking_lunar_radio.move(370,160)
        self.tracking_lunar_radio.setFont(self.bold_font)
        self.tracking_lunar_radio.clicked.connect(self.tracking_btn_state)

        #star selection button
        self.star_selecion = QtWidgets.QPushButton(self)
        self.star_selecion.setText("Star Selection")
        self.star_selecion.setGeometry(QtCore.QRect(370,500,250,100))
        self.star_selecion.setFont(self.bold_font)
        self.star_selecion.setStyleSheet("background-color: cyan")
        self.star_selecion.clicked.connect(self.star_selection_lib)



        #RA and DEC Unit Conversion
        self.ra_dec_units = QtWidgets.QLabel(self)
        self.ra_dec_units.setText(" Coordinate: ")
        self.ra_dec_units.setStyleSheet("background-color: rgb(255,70,70)") 
        self.ra_dec_units.setFont(self.bold_font)
        self.ra_dec_units.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken)
        self.ra_dec_units.move(370,215)    

        #hour and degree decimal button
        self.hr_deg_dec_btn = QRadioButton(self,"Mode Auto")
        self.hr_deg_dec_btn.setText("Decimal")
        self.hr_deg_dec_btn.move(370,260)
        self.hr_deg_dec_btn.setFont(self.bold_font)
        self.hr_deg_dec_btn.clicked.connect(self.unit_button)

        #HH:mm:ss and DD:MM:SS button  
        self.hr_deg_base_60_btn = QRadioButton(self,"Mode Auto")
        self.hr_deg_base_60_btn.setText("hh:mm:ss")
        self.hr_deg_base_60_btn.move(370,290)
        self.hr_deg_base_60_btn.setFont(self.bold_font)
        self.hr_deg_base_60_btn.clicked.connect(self.unit_button)

    #Functions

    def unit_button(self):
        if self.hr_deg_dec_btn.isChecked() is True:
            print("Decimal has been selected")
            self.unit_state = 10
            return self.unit_state 
        elif self.hr_deg_base_60_btn.isChecked() is True:
            print("hh:mm:ss has been selected")
            self.unit_state = 60
            return self.unit_state
        else:
            print("Issue involving unit_button")



    def abort_slew(self):
        self.albert.AbortSlew
        print("Slew Aborted")



    def star_selection_lib(self):
        pass #place library loader here



    def tracking_btn_state(self):
        if self.tracking_sidereal_radio.isChecked() is True:
            print("Sidereal tracking rate has been selected")
            self.albert.TrackingRate = DriveRates.driveSidereal

        elif self.tracking_solar_radio.isChecked()  is True:
            print("Solar tracking rate has been selected")
            self.albert.TrackingRate = DriveRates.driveSolar
            
        elif self.tracking_lunar_radio.isChecked() is True:
            print("Lunar tracking rate has been selected")
            self.albert.TrackingRate = DriveRates.driveLunar    #L for windows and l for Linux

        else:
            print("Issue with tracking_btn_state")



    def updateTime(self):
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
        self.utc_clock_label.setText(f"UTC: {self.time_hour}:{self.time_minute}:{self.time_seconds}")
       


    def get_tele_ip(self):
        #self.albert = Telescope('192.168.1.21:11111',0)
        self.user_ip_address_input, self.ok = QtWidgets.QInputDialog.getText(self, 'Input IP Address', 'IP Address:')
        if self.ok:   #if-statement allows the label to be placed if clicked Okay button
            self.ip_label = QtWidgets.QLabel(self)
            self.ip_label.setText(f"IP Address: {str(self.user_ip_address_input)}")
            self.ip_label.setStyleSheet("background-color: pink")
            self.ip_label.setFont(self.bold_font)
            self.ip_label.setFrameStyle(QtWidgets.QFrame.Panel|QtWidgets.QFrame.Sunken) #label formatting gives depth to labels
            self.ip_label.move(700,50)
            self.ip_label.adjustSize()
            return self.user_ip_address_input
        else:   #If you pressed cancel button or exit button, it exits the entire script
            print("exiting...")
            time.sleep(0.5)
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



    def mount_movement_function(self):
        if self.unit_state == 10:
            ra = float(self.user_ra)
            dec = float(self.user_dec)
            self.ra_dec_bound(ra,dec)
        
        elif self.unit_state == 60:
            self.user_ra_0 = self.user_ra.split('.')   #creates list of items that were separated by a .
            self.user_ra_hr = abs(int(self.user_ra_0[0])) #first list item
            self.user_ra_min = abs(int(self.user_ra_0[1]))#second list item
            self.user_ra_sec = abs(int(self.user_ra_0[2]))#third list item
            self.user_ra = self.user_ra_hr + (self.user_ra_min/60) + (self.user_ra_sec/3600) #converts to decimal form

            self.user_dec_0 = self.user_dec.split('.') #creates list of items that were separated by a .

            if self.user_dec_0[0][0] == '-':   #if statement to catch negative numbers 
                self.user_deg_1 = self.user_dec_0[0][1:]  #grabs first item value and removes minus sign
                self.user_dec_deg = int(self.user_deg_1) #first list item without - sign
                self.user_dec_arcmin =  int(self.user_dec_0[1])#second list item
                self.user_dec_arcsec = int(self.user_dec_0[2]) #third list item
                self.user_dec = (self.user_dec_deg + (self.user_dec_arcmin/60) + ( self.user_dec_arcsec/3600))*-1 #converts to decimal and multiplies by -1 to make it negative
            else:  #assumes its postive. That way, they can either enter + sign or leave it blank
                self.user_dec_deg = abs(int(self.user_dec_0[0]))
                self.user_dec_arcmin =  abs(int(self.user_dec_0[1]))
                self.user_dec_arcsec = abs(int(self.user_dec_0[2])) 
                self.user_dec = self.user_dec_deg + (self.user_dec_arcmin/60) + ( self.user_dec_arcsec/3600)

            ra = self.user_ra 
            dec = self.user_dec
            print(f'Right Ascension in  decimal hours: {ra}')
            print(f'Declination in decimal degrees: {dec}')
            self.ra_dec_bound(ra,dec) #sends ra and dec to function to check boundaries


           
    def ra_dec_bound(self,ra,dec):

        if ra >= self.ra_min and ra < self.ra_max:
            print("Right Ascension is within boundaries")
        else:
            print("Right Ascension is NOT within boundary, try again.")
            del ra, dec  #deletes these values that way it can't be slewed to. Use try and except for this error or make it restart somewhere

        if dec >= self.dec_min and ra <= self.dec_max:
            print("Declination is within boundaries")
        else:
            print("Declination is NOT within boundary, try again.")
            del ra, dec
            
 

        self.albert.SlewToCoordinatesAsync(RightAscension=ra,Declination=dec)
        while(self.albert.Slewing):
            time.sleep(1)
            print("Slewing...")

def window():
    app = QApplication(sys.argv)
    win = Mount_Movement_Win()
    win.setStyleSheet("background-color: rgb(255, 100, 100); color: black") #coral currently
    win.showMaximized()
    #make sure that win shows nicely and exits on click "clean exit"
    sys.exit(app.exec())
window()




#convert UTC to Julian
#add units (hour.minute.second), (degree, arcminute('), arcsecond(''))
#use type(str) or type(float,int) for decision between HH:MM:SS or decimal