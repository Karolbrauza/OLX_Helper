import csv
import os
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
import time
import adModel
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set the URL of the Selenium Grid Hub
grid_url = "http://localhost:4444"

user_data_dir = "C:\\path\\to\\your\\chrome\\user\\data"


# Set the desired capabilities for the browser
capabilities = DesiredCapabilities.CHROME.copy()

def create_webdriver():
    chrome_options = Options()
    # chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    return webdriver.Remote(command_executor=grid_url, options=chrome_options)

def edit_offer(offer):
    logging.info(f"Starting to edit offer {offer.ID}")
    driver = create_webdriver()
    driver.get("https://www.olx.pl/d/mojolx/")
    try:
        navigate_to_offer_edit(driver, offer.ID)
        
        if validate_is_holiday_description(driver, offer, config.holiday_description):
            remove_holiday_description(driver, offer, config.holiday_description)
            revert_offer_price(driver, offer, int(offer.price) - config.price_increase)
        else:
            append_to_offer_description(driver, offer, config.holiday_description)
            change_offer_price(driver, offer, int(offer.price) + config.price_increase)
        
        click_element_by_test_id(driver, "submit-btn")
        time.sleep(3)
    except Exception as e:
        logging.error(f"Error editing offer {offer.ID}: {e}")
    finally:
        time.sleep(5)
        driver.quit()

# Function to perform login and scrape ad list
def login_and_scrape_ads():
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
    driver.quit()

    # Save adList to CSV
    with open('ad_list.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['ID', 'Name', 'Price', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for ad in adList:
            writer.writerow(ad.to_dict())

    return adList

# Function to load ads from CSV
def load_ads_from_csv():
    adList = []
    with open('ad_list.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ad = MarketplaceOffer(row['ID'], row['Name'], row['Price'], row['Description'])
            adList.append(ad)
    return adList

# Main logic
if os.path.exists('ad_list.csv'):
    logging.info("Loading ads from CSV file")
    adList = load_ads_from_csv()
else:
    logging.info("CSV file not found, performing login and scraping ads")
    adList = login_and_scrape_ads()
# Example adList

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = list(executor.map(edit_offer, adList))
#     for future in concurrent.futures.as_completed(futures):
#         try:
#             future.result()
#         except Exception as e:
#             logging.error(f"Error in future: {e}")

# executor.shutdown(wait=True)

# Close the browser
