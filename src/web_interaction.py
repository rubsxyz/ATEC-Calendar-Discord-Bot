import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import os

def setup_driver(config):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--silent')

    chromedriver_path = "/usr/local/bin/chromedriver"
    if not os.path.isfile(chromedriver_path):
        raise FileNotFoundError(f"Chromedriver not found at {chromedriver_path}")
    
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)
    return driver, wait

def login_to_site(driver, wait, config):
    driver.get(config['LOGIN_URL'])
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
