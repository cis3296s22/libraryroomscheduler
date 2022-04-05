

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class TraverseSite:
    def __init__(self, link: str):
        self.link = link
        self.service = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)

    def bookRoom(self, dateStringPath, userN, passW):
        self.driver.get(self.link)
        try:
            timeOption = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, dateStringPath)))
            timeOption.click()
        except:
            print("Room Unavailable/Doesn't Exist")
            return False

        # Continue Booking
        try:
            submitButton = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='submit_times']")))
            submitButton.click()
        except:
            print("Couldn't continue booking")
            return False

        try:
            # Log in  
            userInput = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='username']")))
            userInput.click()
            userInput.send_keys(userN)

            passInput =  WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='password']")))
            passInput.click()
            passInput.send_keys(passW)
            
            logInButton = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-default btn-login']")))
            logInButton.click()
        except:
            print("Login Failure")
            return False

        try:
            # Submit Booking
            submitButton = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='s-lc-eq-bform-submit']")))
            submitButton.click()
        except:
            print("Booking Failure")
            return False
        
        try:
            errorPopUp = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='submit-errors']")))
            # submit-errors
            print("Booking Couldn't be made. Another booking was already made for this day.")
            return False
        except:
            print("Booking Success")
        # Log Out
        jadaSucks = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@id='s-lc-eq-auth-lobtn']")))
        jadaSucks.click()

        return True

    def findRoom(self, dateTime):

        rooms = []

        self.driver.get(self.link)

        try:
            error = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[@class='fc-cell-text']")))
        except:
            print("ERROR NO ELEMENTS LOADED OR DONT EXIST")

        # Fetch all elements with the XPATH "//span..." -> Retrieve all the room numbers, stored in rooms list
        elements = self.driver.find_elements(by=By.XPATH, value="//span[@class='fc-cell-text']")
        for i in elements:
            rooms.append(i.text[0:3])

        grabRoom = False
        roomIndex = 0
        currentRoom = ""

        # Loop through room list until one is available for booking 
        while(not grabRoom and roomIndex < len(rooms)):
            try:
                currentRoom = rooms[roomIndex]

                dateString = (f"//a[@aria-label='{dateTime} - {currentRoom} - Available']")

                timeOption = self.driver.find_element(By.XPATH, dateString)
                print("Room " + currentRoom + " is available")
                grabRoom = True
                return (f"//a[@aria-label='{dateTime} - {currentRoom} - Available']")
            
            except:
                print("Room " + currentRoom + " is not available")
                roomIndex = roomIndex + 1
        return None

