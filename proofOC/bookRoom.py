# https://kivy.org/doc/stable/guide/packaging-osx.html

import logging
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
from kivy.uix.checkbox import CheckBox

import os
import sys
import datetime
import calendar
from loginWindow import login
import csv

from BookingBuilder import BookingBuilder, BookingCreationException
from RepoCommunicator import RepoCommunicator, remoteRepoConfigured, RepositoryConfigurationException

def configurePath(execPath: str):
        """
        Helper to set the proper pathing for the repo dir

        . . .

        Parameters
        ----------
        execPath: str
            The path the application was called from/is running from

        Returns
        ----------
        The path the locl repo should be created in

        """
        # TODO find out why these specifically don't log
        logger = logging.getLogger("appLog")
        logger.debug(f"PATH: {execPath}")
        logger.debug(f"CWD: {os.getcwd()}")
        # TODO change the way's it's checking where it's running from "exe/dist" OR WHEN running 'python3 bookRoom.py' make the user include an argument
        if "dist" in execPath:
            logger.debug("RUNNING FROM EXE")
            return f"{execPath}/../../local_repo"

        else:
            logger.debug("RUNNNG FROM CLI")
            return "local_repo"


class BookingScreen(Screen):
    pass

class P(Screen):
    pass

class TestApp(MDApp):
    """
    The GUI of the application. Extends a Kivy MDApp class.

    . . .


    Methods
    ----------
    build()
        Sets the screen and other necessary parameters at startup
    
    get_time(instance: kivy.MDTimePicker, time: datetime.time)
        Returns the time from the Clock widget
    
    on_time_save(instance: kivy.MDTimePicker, time: datetime.time)
        Formats the time from the Clock widget as a string

    on_time_cancel(instance: kivy.MDTimePicker, time: datetime.time)
        Override on the Clock widget. Does nothing
    
    show_time_picker()
        Binds a Clock widget to the application and displays it upon selection

    on_checkbox_active(instance: kivy.CheckBox, value: bool, Size: str)
        Updates size selection checkboxes
    
    on_date_save(instance: kivy.MDDatePicker, value: datetime, date_range: str)
        Formats the date from the Date picker widget as a string
    
    on_date_cancel(instance: kivy.MDDatePicker, value: datetime)
        Override on the Date widget. Does nothing
    
    show_date_picker()
        Binds a Date picker widget to the application and displays it upon selection

    read_reservations()
        Reads the reservations from the csv file
    
    show_reservations()
        Displays saved reservations
    
    transformData(timeS: str, roomNum: str, date: str)
        Creates a formatted string from the user selections to book a room
    
    display_results(message: str)
        Displays feedback message, generally a success or error message.
    
    hide_results()
        Resets and hides any feedback message
    
    bookRoom(roomSize: str, timeS: str, roomNum: str, date: str, repoUrl: str)
        Takes all the data gathered from the various inputs, saves to file and adds to the repo
    """

    userN=passW=repoUrl=""
    repoPath = configurePath(os.path.dirname(sys.executable))
    repoUrl = remoteRepoConfigured(repoPath)

    def build(self):
        """
        Sets the screen and other necessary parameters at startup

        . . .

        Parameters
        ----------
        None

        Returns
        ----------
        The initial Screen that is displayed to the user

        """
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "200"
        self.theme_cls.theme_style = "Dark"
        root = BookingScreen()
        root.ids.repoUrl.text = self.repoUrl
        return root

    def get_time(self, instance, time):
        """
        Returns the time from the Clock widget

        . . .

        Parameters
        ----------
        instance: kivy.MDTimePicker
            The Clock widget instance
        time: datetime.time
            The time selected from the widget

        Returns
        ----------
        The time from the Clock widget
        """
        return time

    def on_time_save(self, instance, time):
        """
        Sets the screen and other necessary parameters at startup

        . . .

        Parameters
        ----------
        instance: kivy.MDTimePicker
            The Clock Widget instance
        time: datetime.time
            The time selected from the widget

        Returns
        ----------
        None
        """
        formatted_time = time.strftime("%I:%M %p")
        self.root.ids.time.text = str(formatted_time)

    def on_time_cancel(self, instance, time):
        """
        Override on the Clock widget. Does nothing

        . . .

        Parameters
        ----------
        instance: kivy.MDTimePicker
            The Clock Widget instance
        time: datetime.time
            The time selected from the widget

        Returns
        ----------
        None
        """
        # when canceling time selection from the widget don't do anything
        pass

    def show_time_picker(self):
        """
        Binds a Clock widget to the application and displays it upon selection

        . . .

        Parameters
        ----------
        None

        Returns
        ----------
        None
        """
        time_selector = MDTimePicker(accent_color=get_color_from_hex("#BEBEBE"))
        time_selector.bind(on_cancel=self.on_time_cancel, on_save=self.on_time_save, time=self.get_time)
        time_selector.open()

    def on_checkbox_active(self, instance, value, Size):
        """
        Updates size selection checkboxes

        . . .

        Parameters
        ----------
        instance: kivy.CheckBox
            The CheckBox instance
        value: bool
            Selected state, true/false
        Size: str
            The size of the room selected

        Returns
        ----------
        None
        """
        if (value==True):
            self.root.ids.roomSize.text = Size
        if (value==False):
            self.root.ids.roomSize.text = ''

    def on_date_save(self, instance, value, date_range):
        """
        Formats the date from the Date picker widget as a string

        . . .

        Parameters
        ----------
        instance: kivy.MDDatePicker
            The Date picker instance
        value: datetime
            The time returned from the widget
        date_range: str
            Option when selecting a range of dates. Not used but needed to override

        Returns
        ----------
        None
        """
        self.root.ids.date.text = str(value)

    def on_date_cancel(self, instance, value):
        """
        Override on the Date widget. Does nothing

        . . .

        Parameters
        ----------
        instance: kivy.MDDatePicker
            The Date picker instance
        value: datetime
            The time returned from the widget

        Returns
        ----------
        None
        """
        pass

    def show_date_picker(self):
        """
        Binds a Date picker widget to the application and displays it upon selection

        . . .

        Parameters
        ----------
        None

        Returns
        ----------
        None
        """
        date_picker = MDDatePicker()
        date_picker.bind(on_cancel=self.on_date_cancel, on_save=self.on_date_save)
        date_picker.open()
    
    def read_reservations(self):
        """
        Reads the reservations from the csv file

        . . .

        Parameters
        ----------
        None

        Returns
        ----------
        A string containing the content of the csv
        """
        self.fileName = "bookings.csv"
        self.fullPath = f"{self.repoPath}/{self.fileName}"
        count = 0
        content = ""
        with open(self.fullPath, "r") as f:
         reader = csv.reader(f)
         for line in reader:
            if (count != 0):
                #  print(line)
                 content = content + " ".join(map(str, line)) + "\n"
            count = count+1
        return content        
   
    def show_reservations(self):
        """
        Displays saved reservations

        . . .

        Parameters
        ----------
        None

        Returns
        ----------
        None
        """
        show = P()
        popup = Popup(title='Your Reservations', content= show, size_hint = (0.8, 0.8))
        #TODO Implement a back button/more intuitive way to dismiss popup window
        popup.open()

    def transformData(self, timeS, roomNum, date):
        """
        Creates a formatted string from the user selections to book a room

        . . .

        Parameters
        ----------
        timeS: str
            A string representation of the time selected
        roomNum: str
            The room number selected
        date: str
            A string representation of the date selected

        Returns
        ----------
        A formatted string if successful, or None if not
        """
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
            # print(selectTime)
            return selectTime
        except:
            return None

    def display_results(self, message: str):
        """
        Displays feedback message, generally a success or error message.

        . . .

        Parameters
        ----------
        message: str
            The message to display

        Returns
        ----------
        None
        """
        results = self.root.ids.results
        results.text = f"* {message}"
        results.height, results.opacity, results.disabled = '70dp', 100, False

    def hide_results(self):
        """
        Resets and hides any feedback message

        . . .

        Parameters
        ----------
        None

        Returns
        ----------
        None
        """
        results = self.root.ids.results
        results.text = ''
        results.height, results.opacity, results.disabled = 0, 0, True


    def bookRoom(self, roomSize, timeS, roomNum, date, repoUrl):
        """
        Takes all the data gathered from the various inputs, saves to file and adds to the repo

        . . .

        Parameters
        ----------
        roomSize: str
            The size of the room to book
        timeS: str
            The time requested to book the room
        roomNum: str
            The requested room number to book
        date: str
            The date of the booking
        repoUrl: str
            The remote repo url to store the data

        Returns
        ----------
        True if successful, False if an error occurs
        """
        self.hide_results()
        dateString = self.transformData(timeS, roomNum, date)
        if(dateString==None or (roomSize!="small" and roomSize!="large")):
            self.display_results('Incorrect Entry/Format')
            return False

        # save booking to file
        try:
            repo = RepoCommunicator(repoUrl, self.repoPath)
        except RepositoryConfigurationException as e:
            self.display_results(f'{e}')
            return False

        timeS = timeS.strip().lower()
        timeS = "".join(timeS.split()) # removes any inner whitespace
        timeS = timeS if timeS[0] != '0' else timeS[1:] # removes leading zero if present

        try:
            bookings = BookingBuilder(self.userN, self.passW, self.repoPath)
            bookings.addBooking(date, timeS, roomSize)
        except BookingCreationException as e:
            self.display_results(f'{e}')
            return False

        file_names = [
            bookings.fileName,
            '.github/workflows/main.yml',
            'scripts/actionScript.py',
            'scripts/TraverseSite.py',
            'scripts/requirements.txt',
        ]

        try:
            for file in file_names:
                repo.addFile(file)
            repo.pushData()
        except RepositoryConfigurationException as e:
            self.display_results(f'{e}')
            return False

        self.display_results('Data sent to your repo!')
        return True
    
    
        

if __name__ == '__main__':
    logger = logging.getLogger("appLog")
    path = str(os.path.dirname(sys.executable))
    fh = None
    if "venv" in path or "exe" in path:
        # if you're running it right this is either the venv bin or the exe. either way we gotta go up 2 levels
        fh = logging.FileHandler(f'{path}/../../app.log')
    else:
        # otherwise system python. run from where we were called
        fh = logging.FileHandler(f'app.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logger.debug("Application started.")

    userN, passW = login()
    if(userN!=None):
        testApp = TestApp()
        setattr(testApp, 'userN', userN)
        setattr(testApp, 'passW', passW)
        testApp.run()
    else:
        print("Minute has elapsed. Abort.")
