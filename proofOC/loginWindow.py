from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

import time

def login():
    userN = ""
    passW = ""
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument('disable-infobars')
    service = Service(executable_path=ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://tuportal.temple.edu/")
   
    currentUrl = ""
    while(currentUrl!="https://tuportal5.temple.edu/"):
        currentUrl = driver.current_url
        try:
            userN = driver.find_element(By.XPATH, "//input[@id='username']").get_attribute("value")
            passW = driver.find_element(By.XPATH, "//input[@id='password']").get_attribute("value")
        except:
            print(userN, passW)

    driver.quit()
    return userN, passW
        # try:   
        #     timeOption = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-default btn-login']")))
            
        #     userN = driver.find_element(By.XPATH, "//input[@id='username']").get_attribute("value")
        #     passW = driver.find_element(By.XPATH, "//input[@id='password']").get_attribute("value")
        # except:
        #     print("Logged In")
        #     print(driver.current_url)
        #     driver.quit()
            
            
        

# user, passW = login()

# print(user + passW)
