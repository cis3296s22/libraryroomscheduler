# https://kivy.org/doc/stable/guide/packaging-osx.html

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

import time
import datetime
import calendar
import loginWindow

class BookingScreen(Screen):
    pass

class TestApp(App):

    userN=passW=""
   
    def build(self):
        return BookingScreen()
  
    def transformData(self, timeS, roomNum, date):
        try:
            result = list(map(lambda v: v.strip().lower(), [timeS, roomNum, date]))
            if(not timeS or not roomNum or not date):
                return None
            select = datetime.datetime.strptime(result[2], "%m-%d-%Y").date()
            fullDate = select.strftime("%B %d, %Y")
            weekday = calendar.day_name[select.weekday()]
            selectTime = (f"{result[0]} {weekday}, {fullDate} - {result[1]} - Available")
            return selectTime
        except:
            return None
        

    def bookRoom(self, roomSize, timeS, roomNum, date):

        roomSize = roomSize.strip().lower()
        dateString = self.transformData(timeS, roomNum, date)
        if(dateString==None or (roomSize!="small" and roomSize!="large")):
            print('Incorrect Entry/Format')
            return False

        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        # Login to tuportal
        driver.get("https://tuportal.temple.edu/")
        driver.maximize_window()

        driver.find_element(By.XPATH, "//input[@id='username']").send_keys(self.userN)
        driver.find_element(By.XPATH, "//input[@id='password']").send_keys(self.passW)
        driver.find_element(By.XPATH, "//button[@class='btn btn-default btn-login']").click()


        # CHECK LOGIN SUCCESS
        # Wait 30 seconds to detect logout button (Could be login failed screen OR 2FA option)
        try:
            error = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[@class='logout']")))
        except:
            return False
            
        # Go to Charles Libary site (large/small)
        driver.get(f"https://charlesstudy.temple.edu/reserve/charles-{roomSize}")


        try:
            pathOfTime = (f"//a[@aria-label='{dateString}']")
            timeOption = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, pathOfTime)))
            timeOption.click()
        except:
            print("Room Unavailable/Doesn't Exist")
            return False

        # Submit Booking
        submitButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='submit_times']")))
        submitButton.click()

        # Log Out
        jadaSucks = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@id='s-lc-eq-bform-submit']")))
        jadaSucks.click()

        # Exit Driver
        time.sleep(2)
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

    


