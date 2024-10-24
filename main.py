from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from methods import *
import config
import pickle
import time
import adModel
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright

# Set the path to your Chrome driver executable
driver_path = "C:\\webdrivers\\chromedriver-win64\\chromedriver.exe"

# Set the path to your Chrome user data directory
user_data_dir = "C:\\path\\to\\your\\chrome\\user\\data"

# Create Chrome options to use the specified profile
chrome_options = Options()
chrome_options.add_argument(f"user-data-dir={user_data_dir}")

# Create a new instance of the Chrome driver with the specified options
sService = ChromeService(driver_path)
driver = webdriver.Chrome(service=sService, options=chrome_options)

# Navigate to the olx.pl page
driver.get("https://www.olx.pl/d/mojolx/")

# Find the login button and click it
# click_element_by_xpath(driver, '//*[@id="onetrust-accept-btn-handler"]')
# click_element_by_link_text(driver, 'Twoje konto')

# Check if the current URL is https://www.olx.pl/d/mojolx/
if driver.current_url == "https://www.olx.pl/d/mojolx/":
    # Code to execute if the URL matches
    print("The current URL is https://www.olx.pl/d/mojolx/ user is logged in")
else:
    # Code to execute if the URL does not match
    print("The current URL is not https://www.olx.pl/d/mojolx/ user should login")
    send_keys_to_element_by_id(driver, 'username', config.USERNAME)
    send_keys_to_element_by_id(driver, 'password', config.PASSWORD)

    click_element_by_test_id(driver, 'login-submit-button')

time.sleep(3)
driver.get("https://www.olx.pl/d/mojolx/finished")  # Directly go to a logged-in page after adding cookies
time.sleep(3)

# Get list of offers and save them to list 
adList = get_marketplace_offer_list(driver)

holiday_description = " - Jestem na urlopie w związku z czym cena podniesiona o 50zł za fatyge i dodatkowe koszty związane z wysyłką. Pozdrawiam"
price_increase = 50

def process_offer(offer):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"https://www.olx.pl/d/adding/edit/{offer.ID}/?bs=olx_pro_listing")
        
        if validate_is_holiday_description(page, offer, holiday_description):
            remove_holiday_description(page, offer, holiday_description)
            revert_offer_price(page, offer, int(offer.price) - price_increase)
        else:
            append_to_offer_description(page, offer, holiday_description)
            change_offer_price(page, offer, int(offer.price) + price_increase)
        
        page.click('[data-testid="submit-btn"]')
        time.sleep(3)
        browser.close()

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_offer, offer) for offer in adList]
    for future in concurrent.futures.as_completed(futures):
        future.result()

executor.shutdown(wait=True)

# Close the browser
driver.quit()
