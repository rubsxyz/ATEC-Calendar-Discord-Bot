import logging
import sys
import os
from src.discord_bot import start_discord_bot
from src.web_interaction import setup_driver, login_to_site
from src.calendar_interaction import navigate_to_calendar, capture_calendar_image
from src.config import get_config

# Ensure img directory exists
if not os.path.exists("img"):
    os.makedirs("img")

# Logging configuration
logging.basicConfig(level=logging.INFO, filename='bot.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config = get_config()

# Setup driver
driver, wait = setup_driver(config)

# Perform login on the site
if not login_to_site(driver, wait, config):
    logging.warning("Login failed. Trying again...")
    if not login_to_site(driver, wait, config):
        logging.error("Failed to login after two attempts.")
        driver.quit()
        sys.exit(1)

# Navigate to the calendar page
if not navigate_to_calendar(driver, wait):
    logging.error("Failed to navigate to the calendar page.")
    driver.quit()
    sys.exit(1)

# Capture the calendar image
capture_calendar_image(driver)

# Start the Discord bot
start_discord_bot()

# Close the driver
driver.quit()
sys.exit(0)
