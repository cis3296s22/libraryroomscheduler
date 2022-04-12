# https://kivy.org/doc/stable/guide/packaging-osx.html

from turtle import onrelease
from unittest import skip
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.popup import Popup

from kivy.utils import get_color_from_hex

from kivymd.app import MDApp
from kivymd.uix.picker import MDTimePicker
from kivymd.uix.picker import MDDatePicker

import time
import datetime
import calendar
import loginWindow
import csv

from BookingBuilder import BookingBuilder
from RepoCommunicator import RepoCommunicator, remoteRepoConfigured

class BookingScreen(Screen):
    pass

class P(Screen):
    pass

class TestApp(MDApp):

    userN=passW=repoUrl=""
    repoPath = "local_repo"
    repoUrl = remoteRepoConfigured(repoPath)
   
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "200" 
        self.theme_cls.theme_style = "Dark"
        root = BookingScreen()
        root.ids.repoUrl.text = self.repoUrl
        return root

    def get_time(self, instance, time):
        return time

    def on_time_save(self, instance, time):
        formatted_time = time.strftime("%I:%M %p")
        self.root.ids.time.text = str(formatted_time)

    def on_time_cancel(self, instance, time):
        # when canceling time selection from the widget don't do anything
        pass

    def show_time_picker(self):
        time_selector = MDTimePicker(accent_color=get_color_from_hex("#BEBEBE"))
        time_selector.bind(on_cancel=self.on_time_cancel, on_save=self.on_time_save, time=self.get_time)
        time_selector.open()

    def on_date_save(self, instance, value, date_range):
        self.root.ids.date.text = str(value)

    def on_date_cancel(self, instance, value):
        pass

    def show_date_picker(self):
        date_picker = MDDatePicker()
        date_picker.bind(on_cancel=self.on_date_cancel, on_save=self.on_date_save)
        date_picker.open()
    
    def read_reservations(self):
        self.fileName = "bookings.csv"
        self.fullPath = f"local_repo/{self.fileName}"
        count = 0
        content = ""
        with open(self.fullPath, "r") as f:
         reader = csv.reader(f)
         for line in reader:
            if (count != 0):
                 print(line)
                 content = content + " ".join(map(str, line)) + "\n"
            count = count+1
        return content        
   
    def show_reservations(self):
        show = P()
        popup = Popup(title='Your Reservations', content= show, size_hint = (0.8, 0.8))
        #TODO Implement a back button/more intuitive way to dismiss popup window
        popup.open()

    def transformData(self, timeS, roomNum, date):
        try:
            result = list(map(lambda v: v.strip().lower(), [timeS, roomNum, date]))
            if(not timeS or not roomNum or not date):
                return None

            select = datetime.datetime.strptime(result[2], "%Y-%m-%d").date()
            fullDate = select.strftime("%B %d, %Y")
            weekday = calendar.day_name[select.weekday()]

            time = "".join(result[0].split()) # removes any inner whitespace
            time = time if time[0] != '0' else time[1:] # removes leading zero if present

            selectTime = (f"{time} {weekday}, {fullDate} - {result[1]} - Available")
            print(selectTime)
            return selectTime
        except:
            return None
        
        
    
    def bookRoom(self, roomSize, timeS, roomNum, date, repoUrl):

        roomSize = roomSize.strip().lower()
        dateString = self.transformData(timeS, roomNum, date)
        if(dateString==None or (roomSize!="small" and roomSize!="large")):
            print('Incorrect Entry/Format')
            return False

        # save booking to file
        repo = RepoCommunicator(repoUrl, self.repoPath)

        timeS = timeS.strip().lower()
        timeS = "".join(timeS.split()) # removes any inner whitespace
        timeS = timeS if timeS[0] != '0' else timeS[1:] # removes leading zero if present
    

        bookings = BookingBuilder(self.userN, self.passW)
        bookings.addBooking(date, timeS, roomSize)

        repo.addFile(bookings.fileName)
        repo.addFile('.github/workflows/main.yml')
        repo.addFile('scripts/actionScript.py')
        repo.addFile('scripts/TraverseSite.py')
        repo.addFile('scripts/requirements.txt')
        repo.pushData()

        return True
    
    
        

if __name__ == '__main__':
    userN, passW = loginWindow.login()
    if(userN!=None):
        testApp = TestApp()
        setattr(testApp, 'userN', userN)
        setattr(testApp, 'passW', passW)
        testApp.run()
    else:
        print("Minute has elapsed. Abort.")

    


