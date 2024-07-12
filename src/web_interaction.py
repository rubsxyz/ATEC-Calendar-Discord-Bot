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
    chromedriver_path = "/usr/local/bin/chromedriver"
    logging.info(f"Using ChromeDriver path: {chromedriver_path}")
    
    if not os.path.isfile(chromedriver_path):
        logging.error(f"ChromeDriver does not exist at path: {chromedriver_path}")
        raise FileNotFoundError(f"No such file: '{chromedriver_path}'")
    
    logging.info(f"ChromeDriver Permissions: {oct(os.stat(chromedriver_path).st_mode)}")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--disable-sync")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--metrics-recording-only")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-crash-reporter")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--single-process")
    
    service = Service(executable_path=chromedriver_path)
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