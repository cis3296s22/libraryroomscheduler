from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def login():
    start = time.time()
    userN = ""
    passW = ""
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('start-maximized')
    service = Service(executable_path=ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.get("https://tuportal.temple.edu/")
   
    currentUrl = ""
    while(currentUrl!="https://tuportal5.temple.edu/"):
        currentUrl = driver.current_url
        timeElapsed = round(time.time()-start)
        if(timeElapsed==60):
            userN = passW = None
            break
        
        try:
            userN = driver.find_element(By.XPATH, "//input[@id='username']").get_attribute("value")
            passW = driver.find_element(By.XPATH, "//input[@id='password']").get_attribute("value")
        except:
            pass

    driver.quit()
    return userN, passW
