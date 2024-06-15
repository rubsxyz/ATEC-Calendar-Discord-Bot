import logging
import re
import sys
import os
from selenium import webdriver  # type: ignore
from selenium.webdriver.chrome.service import Service  # type: ignore
from selenium.webdriver.chrome.options import Options  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.common.keys import Keys  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
from selenium.webdriver.support import expected_conditions as EC  # type: ignore
from selenium.webdriver.common.action_chains import ActionChains  # type: ignore
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException  # type: ignore
from PIL import Image  # type: ignore
import discord  # type: ignore
import aiohttp  # type: ignore
import asyncio
import time
from dotenv import load_dotenv # type: ignore

# Load environment variables from .env file
load_dotenv()

# Logging configuration
logging.basicConfig(level=logging.INFO, filename='bot.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables with unique names
LOGIN_URL = os.getenv('LOGIN_URL')
USER_NAME = os.getenv('USER_NAME')  # Changed from USERNAME to USER_NAME
USER_PASSWORD = os.getenv('USER_PASSWORD')  # Changed from PASSWORD to USER_PASSWORD
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

# Verify environment variables are loaded correctly
logging.info(f"LOGIN_URL: {LOGIN_URL}")
logging.info(f"USER_NAME: {USER_NAME}")
logging.info(f"USER_PASSWORD: {USER_PASSWORD}")
logging.info(f"DISCORD_TOKEN: {DISCORD_TOKEN}")
logging.info(f"CHANNEL_ID: {CHANNEL_ID}")

# Selenium configuration to capture the image
chrome_options = Options()
chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Path to Google Chrome executable
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument('--log-level=3')  # Set log level to 3 (FATAL) to reduce logging
chrome_options.add_argument('--silent')  # Add silent option to suppress logging

# Ensure the path to the downloaded chromedriver is correct
service = Service(executable_path="D:/chromedriver-win64/chromedriver.exe")  # Path to ChromeDriver executable
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)

# Function to perform login
def login_to_site(login_url, username, password):
    driver.get(login_url)
    logging.info("Login page loaded.")

    try:
        # Explicit wait for login fields
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

        # Explicit wait for the page after login
        wait.until(EC.url_contains("DesktopDefault"))
        logging.info("Login successful.")
        return True

    except TimeoutException:
        logging.error("Timeout while trying to login.")
        return False

# Function to navigate to the calendar page and click the "Agenda Pessoal" link
def navigate_to_calendar():
    try:
        # Explicit wait for the main page after login
        wait.until(EC.presence_of_element_located((By.ID, "li_942")))

        # Hover over the dropdown menu to reveal the "Agenda" link
        logging.info("Trying to locate the dropdown menu.")
        dropdown_menu = wait.until(EC.visibility_of_element_located((By.ID, "li_942")))  # Replace with the correct dropdown menu ID
        ActionChains(driver).move_to_element(dropdown_menu).perform()
        logging.info("Mouse moved over the dropdown menu.")

        # Wait to ensure the "Agenda Pessoal" link is interactive
        # time.sleep(1)

        # Click the "Agenda Pessoal" link
        logging.info("Trying to locate the 'Agenda Pessoal' link.")
        agenda_link = wait.until(EC.element_to_be_clickable((By.ID, "link_level0_943")))  # Replace with the correct agenda link ID
        agenda_link.click()
        logging.info("Clicked on the 'Agenda Pessoal' link.")

        # # Wait for the new page to load
        # time.sleep(10) # Adjust as needed for loading time

        # Get the current window handle and switch to the new window if opened
        current_window = driver.current_window_handle
        window_handles = driver.window_handles
        for handle in window_handles:
            if handle != current_window:
                driver.switch_to.window(handle)
                break

        # Ensure the new page has loaded
        wait.until(EC.presence_of_element_located((By.ID, "ctl00_details")))  # Replace with the ID of an element present on the calendar page
        logging.info("Calendar page loaded successfully.")

        # Maximize the window before taking a screenshot
        driver.maximize_window()
        driver.set_window_size(1920, 1000)  # Ensure the window is large enough to capture the entire calendar

        return True

    except (TimeoutException, ElementNotInteractableException) as e:
        logging.error(f"Failed to load the calendar page: {e}")
        return False

# Function to capture the calendar image
def capture_calendar_image():
    try:
        time.sleep(1)  # Time for the calendar page to fully load classes
        driver.save_screenshot("calendar_screenshot.png")
        # Optionally crop the image to include only the calendar
        img = Image.open("calendar_screenshot.png")
        # Define the correct coordinates to crop the image
        left, top, right, bottom = 50, 180, 1860, 900
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

# Perform login on the site
if not login_to_site(LOGIN_URL, USER_NAME, USER_PASSWORD):
    logging.warning("Login failed. Trying again...")
    if not login_to_site(LOGIN_URL, USER_NAME, USER_PASSWORD):
        logging.error("Failed to login after two attempts.")
        driver.quit()
        sys.exit(1)

# Navigate to the calendar page
if not navigate_to_calendar():
    logging.error("Failed to navigate to the calendar page.")
    driver.quit()
    sys.exit(1)

# Capture the calendar image
capture_calendar_image()

# Start the Discord bot
start_discord_bot()

# Close the driver
driver.quit()
sys.exit(0)
