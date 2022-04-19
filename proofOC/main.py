from selenium import webdriver

from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import os
import sys
import getpass
import time
import datetime
import calendar

from RepoCommunicator import RepoCommunicator, remoteRepoConfigured
from BookingBuilder import BookingBuilder


def login(user, passW, dateString, roomSize):
    

    # Login to tuportal
    driver.get("https://tuportal.temple.edu/")
    driver.maximize_window()

    driver.find_element(By.XPATH, "//input[@id='username']").send_keys(user)
    driver.find_element(By.XPATH, "//input[@id='password']").send_keys(passW)
    driver.find_element(By.XPATH, "//button[@class='btn btn-default btn-login']").click()

    # If login fails check for error
    
    try:
        # Wait 30 seconds to detect logout button (Could be login failed screen OR 2FA option)
        error = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[@class='logout']")))
    except:
        print("Incorrect Credentials")
        return False


    roomS = "https://charlesstudy.temple.edu/reserve/charles-"
    roomS = roomS+"small" if roomSize=="small" else roomS+"large" if roomSize=="large" else roomS+"error"

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
    logoutButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@id='s-lc-eq-auth-lobtn']")))
    logoutButton.click()

    # Make Another Booking - Element xpath ://a[@href='/reserve/charles-small'] [@class='btn btn-primary']
   
    # Exit driver
    time.sleep(2)
    return True


def transformData(timeS, roomNum, date):
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
    select = datetime.datetime.strptime(date, "%m-%d-%Y").date()
    fullDate = select.strftime("%B %d, %Y")
    weekday = calendar.day_name[select.weekday()]
    selectTime = (timeS + " " + weekday + ", " + fullDate + " - " + roomNum + " - Available")
    return selectTime



# Instead of having the driver downloaded and in the folder :
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


try:
    # User input (username, password, booking details)
    repoPath = "local_repo"
    repoUrl = remoteRepoConfigured(repoPath)
    if not repoUrl:
        repoUrl = input("Enter clone URL for GitHub repo: ")

    user = input("Enter TU User: ")
    passW = getpass.getpass("Enter Password: ")
    dateC = input("Enter Date of Booking [FORMAT MM-dd-YYYY]: ")
    roomSize = (input("Enter Room Size: [LARGE or SMALL]: ")).lower()
    room = input("Enter Room #: ")
    timeSlot = input("Enter Time [FORMAT H:MMpm or H:MMam]: ")

    repo = RepoCommunicator(repoUrl, repoPath)
    bookings = BookingBuilder(user, passW)

    dateString = transformData(timeSlot, room, dateC)

    bookings.addBooking(dateString, roomSize)

    repo.addFile(bookings.fileName)
    repo.pushData()

    login(user, passW, dateString, roomSize)


except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)

finally:
    driver.quit()