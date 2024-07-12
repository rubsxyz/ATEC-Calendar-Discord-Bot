import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

def setup_driver(config):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--remote-debugging-port=9222')

    service = Service(executable_path="/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)
    return driver, wait

def login_to_site(driver, wait, config):
    driver.get('https://trainingserver.atec.pt/trainingserver/')
    logging.info("Login page loaded.")
    
    try:
        user_field = wait.until(EC.presence_of_element_located((By.ID, "txtUser")))
        pass_field = wait.until(EC.presence_of_element_located((By.ID, "txtPwd")))
        
        user_field.send_keys(config['USER_NAME'])
        pass_field.send_keys(config['USER_PASSWORD'])
        pass_field.send_keys(Keys.RETURN)
        logging.info("Login credentials sent.")
        
        wait.until(EC.url_contains("DesktopDefault"))
        logging.info("Login successful.")
        return True
    except TimeoutException:
        logging.error("Timeout while trying to login.")
        return False