from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def login(*creds: str):
    """
    Used to collect credentials for the application to book rooms at a later date

    . . .

    Parameters
    ----------
    creds: str, optional
        Credentials to attempt a login with automatically

    Returns
    ----------
    The Temple username and password used to log in
    """
    start = time.time()
    userN = ""
    passW = ""
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('start-maximized')
    if creds:
        chrome_options.headless = True
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
            if creds:
                userN = creds[0]
                passW = creds[1]
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='username']"))).send_keys(userN)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='password']"))).send_keys(passW)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-default btn-login']"))).click()
        
            userN = driver.find_element(By.XPATH, "//input[@id='username']").get_attribute("value")
            passW = driver.find_element(By.XPATH, "//input[@id='password']").get_attribute("value")
        except:
            pass

    driver.quit()
    return userN, passW
