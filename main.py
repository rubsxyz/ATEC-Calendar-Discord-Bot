import logging
import re
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from PIL import Image
import discord
import aiohttp
import asyncio
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Logging configuration
logging.basicConfig(level=logging.INFO, filename='bot.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Selenium configuration to capture the image
chrome_options = Options()
chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x3000")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--silent')

# Ensure the path to the downloaded chromedriver is correct
service = Service(executable_path="D:/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 60)

# Login URL and login information
login_url = os.getenv("LOGIN_URL")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Function to perform login
def login_to_site(login_url, username, password):
    driver.get(login_url)
    logging.info("Login page loaded.")
    try:
        user_field = wait.until(EC.presence_of_element_located((By.ID, "txtUser")))
        pass_field = wait.until(EC.presence_of_element_located((By.ID, "txtPwd")))

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

# Function to navigate to the calendar page and click the "Agenda Pessoal" link
def navigate_to_calendar():
    try:
        wait.until(EC.presence_of_element_located((By.ID, "li_942")))
        logging.info("Trying to locate the dropdown menu.")
        dropdown_menu = wait.until(EC.visibility_of_element_located((By.ID, "li_942")))
        ActionChains(driver).move_to_element(dropdown_menu).perform()
        logging.info("Mouse moved over the dropdown menu.")
        time.sleep(1)
        logging.info("Trying to locate the 'Agenda Pessoal' link.")
        agenda_link = wait.until(EC.element_to_be_clickable((By.ID, "link_level0_943")))
        agenda_link.click()
        logging.info("Clicked on the 'Agenda Pessoal' link.")
        time.sleep(10)
        current_window = driver.current_window_handle
        for handle in driver.window_handles:
            if handle != current_window:
                driver.switch_to.window(handle)
                break
        wait.until(EC.presence_of_element_located((By.ID, "ctl00_details")))
        logging.info("Calendar page loaded successfully.")
        driver.maximize_window()
        return True
    except (TimeoutException, ElementNotInteractableException) as e:
        logging.error(f"Failed to load the calendar page: {e}")
        return False

# Function to capture the calendar image
def capture_calendar_image():
    try:
        time.sleep(10)
        driver.save_screenshot("calendar_screenshot.png")
        img = Image.open("calendar_screenshot.png")
        left, top, right, bottom = 0, 0, img.width, img.height
        cropped_img = img.crop((left, top, right, bottom))
        cropped_img.save("calendar_screenshot_cropped.png")
        logging.info("Calendar image captured successfully.")
    except Exception as e:
        logging.error(f"Error capturing the calendar image: {e}")

# Discord bot configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

class MyClient(discord.Client):
    async def on_ready(self):
        logging.info(f'Logged in as {self.user}')
        await self.send_calendar_image()
        await self.close()

    async def send_calendar_image(self):
        try:
            channel = self.get_channel(CHANNEL_ID)
            async with aiohttp.ClientSession() as session:
                with open("calendar_screenshot_cropped.png", "rb") as f:
                    file = discord.File(f, filename="calendar_screenshot_cropped.png")
                    await channel.send(file=file)
            logging.info("Calendar image sent successfully.")
        except Exception as e:
            logging.error(f"Error sending the calendar image: {e}")

def start_discord_bot():
    intents = discord.Intents.default()
    client = MyClient(intents=intents)
    try:
        client.run(DISCORD_TOKEN)
    except Exception as e:
        logging.error(f"Error running the Discord bot: {e}")
        sys.exit(1)

if not login_to_site(login_url, username, password):
    logging.warning("Login failed. Trying again...")
    if not login_to_site(login_url, username, password):
        logging.error("Failed to login after two attempts.")
        driver.quit()
        sys.exit(1)

if not navigate_to_calendar():
    logging.error("Failed to navigate to the calendar page.")
    driver.quit()
    sys.exit(1)

capture_calendar_image()
start_discord_bot()
driver.quit()
sys.exit(0)
