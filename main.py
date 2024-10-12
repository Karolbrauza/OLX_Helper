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

adList = get_marketplace_offer_list(driver)

navigate_to_offer_edit(driver, adList[0].ID)
get_offer_description(driver, adList[0])
append_to_offer_description(driver, adList[0], " - Jestem na urlopie w związku z czym cena podniesiona o 50zł za fatyge i dodatkowe koszty związane z wysyłką. Pozdrawiam")
change_offer_price(driver, adList[0], int(adList[0].price) + 50)

time.sleep(3)


# Close the browser
driver.quit()