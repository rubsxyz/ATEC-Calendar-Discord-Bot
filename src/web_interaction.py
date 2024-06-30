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
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--remote-debugging-port=9222')

    driver = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver'), options=chrome_options)
    wait = WebDriverWait(driver, 10)
    return driver, wait

def login_to_site(driver, wait, config):
    login_url = config['LOGIN_URL']
    username = config['USER_NAME']
    password = config['USER_PASSWORD']
    
    driver.get(login_url)
    logging.info("Login page loaded.")

    try:
        logging.info("Waiting for user field...")
        user_field = wait.until(EC.presence_of_element_located((By.ID, "txtUser")))
        logging.info("User field located.")
        logging.info("Waiting for password field...")
        pass_field = wait.until(EC.presence_of_element_located((By.ID, "txtPwd")))
        logging.info("Password field located.")

        logging.info(f"Username: {username}")
        logging.info(f"Password: {password}")

        user_field.send_keys(username)
        pass_field.send_keys(password)
        pass_field.send_keys(Keys.RETURN)
        logging.info("Login credentials sent.")

        wait.until(EC.url_contains("DesktopDefault"))
        logging.info("Login successful.")
        return True
    except TimeoutException:
        logging.error("Timeout while trying to login.")
        return False
