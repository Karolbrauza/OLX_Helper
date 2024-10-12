import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Set the path to your Chrome driver executable
driver_path = "C:\\webdrivers\\chromedriver-win64\\chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Navigate to the olx.pl page (this must match the domain the cookies were saved for)
driver.get("https://www.olx.pl/")

# Load cookies from the file
with open("cookies.pkl", "rb") as file:
    cookies = pickle.load(file)

# Apply each cookie to the current session
for cookie in cookies:
    # Print each cookie to verify
    print(f"Adding cookie: {cookie}")
    driver.add_cookie(cookie)

# Refresh the page to apply cookies
driver.get("https://www.olx.pl/d/mojolx/")  # Directly go to a logged-in page after adding cookies

# Check the cookies after refresh
current_cookies = driver.get_cookies()
print("Current cookies after refresh:")
for cookie in current_cookies:
    print(cookie)

# Verify if the user is logged in
driver.implicitly_wait(5)  # Give it time to refresh and load
print("Page refreshed, check if login was successful.")

# Close the browser
driver.quit()
