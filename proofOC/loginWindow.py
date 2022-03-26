from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options



def login():
    max = 6
    attempts = 0
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument('disable-infobars')
    service = Service(executable_path=ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://tuportal.temple.edu/")
    
    while(True):
        
        # Need to get user login info

        try:
            attempts+=1
            timeOption = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='logout']")))
            print("Successful Login")
            driver.quit()
            return userN, passW
        except:
            tries = max-attempts
            if(tries==0):
                print("Abort.")
                driver.quit()
                return False
            else:
                tryString = "try" if (tries==1) else "tries"
                print("Waiting: %d more %s..." % (tries, tryString))






userN, passW = login()

print("Final __ " + userN + " __")
print("Final __ " + passW + " __")

