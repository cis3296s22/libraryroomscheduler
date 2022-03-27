# https://kivy.org/doc/stable/guide/packaging-osx.html


from selenium import webdriver


from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from kivy.app import App


from selenium.webdriver.chrome.options import Options
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

import time
import datetime
import calendar

import loginWindow


class BookingScreen(Screen):
    pass

class LoginScreen(Screen):
    pass



class TestApp(App):
    sm = ScreenManager(transition = NoTransition())
    loginScreen = None
    bookingScreen = None
    loginFail = False

    userN = passW = ""

    def transformData(self, timeS, roomNum, date):
        result = list(map(lambda v: v.strip().lower(), [timeS, roomNum, date]))
  
        for i in result:
            print("-- " + i + " --")

        select = datetime.datetime.strptime(result[2], "%m-%d-%Y").date()
        fullDate = select.strftime("%B %d, %Y")
        weekday = calendar.day_name[select.weekday()]
        selectTime = (result[0] + " " + weekday + ", " + fullDate + " - " + result[1] + " - Available")
        return selectTime


    def bookRoom(self, roomSize, timeS, roomNum, date):
        # SETUP DRIVER / LOGIN
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        service = Service(executable_path=ChromeDriverManager().install())
        # driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        driver = webdriver.Chrome(service=service)
        # Login to tuportal
        driver.get("https://tuportal.temple.edu/")
        driver.maximize_window()

        driver.find_element(By.XPATH, "//input[@id='username']").send_keys(self.userN)
        driver.find_element(By.XPATH, "//input[@id='password']").send_keys(self.passW)
        driver.find_element(By.XPATH, "//button[@class='btn btn-default btn-login']").click()

        dateString = self.transformData(timeS, roomNum, date)

        # CHECK LOGIN SUCCESS
        try:
            # Wait 30 seconds to detect logout button (Could be login failed screen OR 2FA option)
            error = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[@class='logout']")))
        except:
            print("Incorrect Credentials")
            return False

        roomSize = roomSize.strip().lower()
        roomS = (f"https://charlesstudy.temple.edu/reserve/charles-{roomSize}")
        print(roomS)
        

        try:
            driver.get(roomS)
        except: 
            print("Couldn't load library page")


        
        # Check to see if loaded - may be unavailable after first time caues temple pages make it unavailable even if not booked - only when clicked
        # 8:00am Thursday, March 17, 2022 - 383 - Unavailable/Padding
        try:
            pathOfTime = "//a[@aria-label='" + dateString + "']"
            timeOption = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, pathOfTime)))
            timeOption.click()
        except:
            print("Room unavailable")
            return False


        # Submit Booking
        submitButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='submit_times']")))
        submitButton.click()


        # LOGOUT
        # logoutButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@id='s-lc-eq-auth-lobtn']")))
        # logoutButton.click()

        # Make Another Booking - Element xpath ://a[@href='/reserve/charles-small'] [@class='btn btn-primary']
        
        yourMomButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@id='s-lc-eq-bform-submit']")))
        yourMomButton.click()

        # Exit driver
        time.sleep(2)
        return True
  
    
    def switchPage(self, screen):
        self.sm.switch_to(screen)


    def login(self, userN, passW):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        service = Service(executable_path=ChromeDriverManager().install())
        # driver = webdriver.Chrome(service=service, options=chrome_options)
        driver = webdriver.Chrome(service=service)
 
        driver.get("https://tuportal.temple.edu/")
        driver.find_element(By.XPATH, "//input[@id='username']").send_keys(userN)
        driver.find_element(By.XPATH, "//input[@id='password']").send_keys(passW)
        driver.find_element(By.XPATH, "//button[@class='btn btn-default btn-login']").click()

        try:
            error = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='logout']")))
        except:
            self.loginFail = True

        if(not self.loginFail):
            self.switchPage(self.bookingScreen)
            self.userN = userN
            self.passW = passW
            print("Successful Login")
            
        else:
            print("Login Error")
        
        # Reset login attempt
        self.loginFail = False


    def build(self):
        # self.loginScreen = LoginScreen(name='login')
        self.bookingScreen = BookingScreen(name='booking')
        # self.sm.add_widget(self.loginScreen)
        self.sm.add_widget(self.bookingScreen)
        return self.sm

if __name__ == '__main__':
    if(loginWindow.login()):
        TestApp().run()

    


