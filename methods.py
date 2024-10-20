from operator import contains
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from adModel import MarketplaceOffer

def wait_for_element(driver, by, value, timeout=10):
    try:
        element_present = EC.presence_of_element_located((by, value))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print(f"Timed out waiting for element: {value}")

def click_element_by_link_text(driver, link_text):
    try:
        wait_for_element(driver, By.PARTIAL_LINK_TEXT, link_text)
        element = driver.find_element(By.PARTIAL_LINK_TEXT, link_text)
        element.click()
    except NoSuchElementException:
        print(f"Element with link text '{link_text}' not found.")
        
def click_element_by_text(driver, text):
    try:
        # Find all elements on the page
        elements = driver.find_elements_by_xpath(f"//*[contains(text(), '{text}')]")
        
        # Iterate through the elements and click the first one containing the text
        if elements:
            elements[0].click()
            print(f"Clicked element containing text: {text}")
            return True
        else:
            print(f"No element found containing the text: {text}")
            return False
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        return False

def click_element_by_id(driver, element_id):
    try:
        wait_for_element(driver, By.ID, element_id)
        element = driver.find_element(By.ID, element_id)
        element.click()
    except NoSuchElementException:
        print(f"Element with ID '{element_id}' not found.")

def click_element_by_xpath(driver, xpath):
    try:
        wait_for_element(driver, By.XPATH, xpath)
        element = driver.find_element(By.XPATH, xpath)
        element.click()
    except NoSuchElementException:
        print(f"Element with XPath '{xpath}' not found.")

def send_keys_to_element_by_id(driver, element_id, keys):
    try:
        wait_for_element(driver, By.ID, element_id)
        element = driver.find_element(By.ID, element_id)
        element.send_keys(keys)
    except NoSuchElementException:
        print(f"Element with ID '{element_id}' not found.")

def click_element_by_test_id(driver, test_id):
    try:
        wait_for_element(driver, By.CSS_SELECTOR, f'[data-testid="{test_id}"]')
        element = driver.find_element(By.CSS_SELECTOR, f'[data-testid="{test_id}"]')
        element.click()
    except NoSuchElementException:
        print(f"Element with data-testid '{test_id}' not found.")

def get_ad_list(driver):
    try:
        wait_for_element(driver, By.CSS_SELECTOR, f'[data-testid="ad-row"]')
        elements = driver.find_elements(By.CSS_SELECTOR, f'[data-testid="ad-row"]')
        return elements
    except NoSuchElementException:
        print(f"Elements with data-testid ad-row not found.")
        return []
    
def get_marketplace_offer_list(driver):
    ad_elements = get_ad_list(driver)
    offers = []
    for ad_element in ad_elements:
        try:
            ad_id_element = ad_element.find_element(By.CSS_SELECTOR, '[data-cy="ad-id"]')
            ad_id_text = ad_id_element.text
            ad_id = ad_id_text.split(":")[1].strip()
            
            ad_name_element = ad_element.find_element(By.CSS_SELECTOR, '[data-cy="inventory-title"]')
            ad_name = ad_name_element.text
            
            ad_price_element = ad_element.find_element(By.CSS_SELECTOR, '[data-cy="inventory-item-price"]')
            ad_price_text = ad_price_element.text
            ad_price = ad_price_text.split("zł")[0].strip().replace(" ", "")
            
            offer = MarketplaceOffer(ID=ad_id, name=ad_name, price=ad_price)
            offers.append(offer)
        except NoSuchElementException:
            print("Ad ID, name, or price element not found in one of the ad elements.")
    return offers

def navigate_to_offer_edit(driver, offer_id):
    edit_url = f"https://www.olx.pl/d/adding/edit/{offer_id}/?bs=olx_pro_listing"
    driver.get(edit_url)

def get_offer_description(driver, offer):
    try:
        wait_for_element(driver, By.CSS_SELECTOR, '[data-cy="posting-description"]')
        description_element = driver.find_element(By.CSS_SELECTOR, '[data-cy="posting-description"]')
        offer.description = description_element.text
        return offer.description
    except NoSuchElementException:
        print("Description element not found.")

def validate_is_holiday_description(driver, offer, holiday_description):
    current_description = get_offer_description(driver, offer)
    
    if holiday_description in current_description:
        return True
    else:
        return False

def append_to_offer_description(driver, offer, additional_text):
    try:
        wait_for_element(driver, By.CSS_SELECTOR, '[data-cy="posting-description"]')
        description_element = driver.find_element(By.CSS_SELECTOR, '[data-cy="posting-description"]')
        current_description = description_element.text
        new_description = current_description + " " + additional_text
        description_element.clear()
        description_element.send_keys(new_description)
        offer.description = new_description
    except NoSuchElementException:
        print("Description element not found.")

def change_offer_price(driver, offer, new_price):
    try:
        wait_for_element(driver, By.CSS_SELECTOR, '[data-cy="posting-price"]')
        price_element = driver.find_element(By.CSS_SELECTOR, '[data-cy="posting-price"]')
        price_element.send_keys(Keys.CONTROL + "a")
        price_element.send_keys(Keys.DELETE)
        price_element.send_keys(new_price)
        offer.price = new_price
    except NoSuchElementException:
        print("Price element not found.")
