from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from methods import *
import config
import pickle
import time
import adModel
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set the URL of the Selenium Grid Hub
grid_url = "http://localhost:4444/wd/hub"

# Set the desired capabilities for the browser
capabilities = DesiredCapabilities.CHROME.copy()

def create_webdriver():
    return webdriver.Remote(command_executor=grid_url, desired_capabilities=capabilities)

def edit_offer(offer):
    driver = create_webdriver()
    try:
        navigate_to_offer_edit(driver, offer.ID)
        
        if validate_is_holiday_description(driver, offer, holiday_description):
            remove_holiday_description(driver, offer, holiday_description)
            revert_offer_price(driver, offer, int(offer.price) - price_increase)
        else:
            append_to_offer_description(driver, offer, holiday_description)
            change_offer_price(driver, offer, int(offer.price) + price_increase)
        
        click_element_by_test_id(driver, "submit-btn")
        time.sleep(3)
    except Exception as e:
        logging.error(f"Error editing offer {offer.ID}: {e}")
    finally:
        driver.quit()

# Create a new instance of the WebDriver
driver = create_webdriver()

# Navigate to the olx.pl page
driver.get("https://www.olx.pl/d/mojolx/")

# Check if the current URL is https://www.olx.pl/d/mojolx/
if driver.current_url == "https://www.olx.pl/d/mojolx/":
    logging.info("The current URL is https://www.olx.pl/d/mojolx/ user is logged in")
else:
    logging.info("The current URL is not https://www.olx.pl/d/mojolx/ user should login")
    send_keys_to_element_by_id(driver, 'username', config.USERNAME)
    send_keys_to_element_by_id(driver, 'password', config.PASSWORD)
    click_element_by_test_id(driver, 'login-submit-button')

time.sleep(3)
driver.get("https://www.olx.pl/d/mojolx/finished")
time.sleep(3)

# Get list of offers and save them to list 
adList = get_marketplace_offer_list(driver)

holiday_description = " - Jestem na urlopie w związku z czym cena podniesiona o 50zł za fatyge i dodatkowe koszty związane z wysyłką. Pozdrawiam"
price_increase = 50

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(edit_offer, offer) for offer in adList]
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()
        except Exception as e:
            logging.error(f"Error in future: {e}")

executor.shutdown(wait=True)

# Close the browser
driver.quit()
