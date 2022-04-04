

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

class Scheduler:

    def __init__(self):
        thing = "hello"

    def findRoom(self):
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        rooms = []

        driver.get("https://charlesstudy.temple.edu/reserve/charles-small")

        try:
            error = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[@class='fc-cell-text']")))
        except:
            print("ERROR NO ELEMENTS LOADED OR DONT EXIST")

        # Fetch all elements with the XPATH "//span..." -> Retrieve all the room numbers, stored in rooms list
        elements = driver.find_elements(by=By.XPATH, value="//span[@class='fc-cell-text']")
        for i in elements:
            rooms.append(i.text[0:3])

        grabRoom = False
        roomIndex = 0
        currentRoom = ""

        # Loop through room list until one is available for booking 
        while(not grabRoom and roomIndex < len(rooms)):
            try:
                currentRoom = rooms[roomIndex]

                # TODO Change so it's not hardcoded 
                # Should read in from csv file 
                dateString = (f"//a[@aria-label='1:00pm Tuesday, April 5, 2022 - {currentRoom} - Available']")
                timeOption = driver.find_element(By.XPATH, dateString)
                print("Room " + currentRoom + " is available")
                grabRoom = True
                return currentRoom
            
            except:
                print("Room " + currentRoom + " is not available")
                roomIndex = roomIndex + 1


        return None


sc = Scheduler()
sc.findRoom()