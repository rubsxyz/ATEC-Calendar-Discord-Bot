import time
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException

def navigate_to_calendar(driver, wait):
    try:
        wait.until(EC.presence_of_element_located((By.ID, "li_942")))
        dropdown_menu = wait.until(EC.visibility_of_element_located((By.ID, "li_942")))
        ActionChains(driver).move_to_element(dropdown_menu).perform()
        agenda_link = wait.until(EC.element_to_be_clickable((By.ID, "link_level0_943")))
        agenda_link.click()
        
        current_window = driver.current_window_handle
        for handle in driver.window_handles:
            if handle != current_window:
                driver.switch_to.window(handle)
                break
        wait.until(EC.presence_of_element_located((By.ID, "ctl00_details")))
        driver.maximize_window()
        driver.set_window_size(1920, 1000)
        return True
    except (TimeoutException, ElementNotInteractableException) as e:
        logging.error(f"Failed to load the calendar page: {e}")
        return False

##### TODO ######
# def navigate_to_next_calendar(driver, wait):
#     try:
#         navigate_to_calendar()
#         proxima_semana = wait.until(EC.element_to_be_clickable((By.ID, "link_level0_943")))
#         proxima_semana.click()
#         return True

#     except (TimeoutException, ElementNotInteractableException) as e:
#         logging.error(f"Failed to load the calendar page: {e}")
#         return False

def capture_calendar_image(driver):
    try:
        time.sleep(1)  # Time for the calendar page to fully load
        driver.save_screenshot("images/calendar_screenshot.png")
        img = Image.open("images/calendar_screenshot.png")
        left, top, right, bottom = 50, 180, 1860, 900
        cropped_img = img.crop((left, top, right, bottom))
        cropped_img.save("images/calendar_screenshot_cropped.png")
        logging.info("Calendar image captured successfully.")
    except Exception as e:
        logging.error(f"Error capturing the calendar image: {e}")
