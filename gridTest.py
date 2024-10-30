import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import os

# List of URLs to visit
urls = [
    "https://www.olx.pl/d/mojolx/",
    "https://www.olx.pl/d/mojolx/",
    "https://www.olx.pl/d/mojolx/",
    "https://www.olx.pl/d/mojolx/",
    "https://www.olx.pl/d/mojolx/"
]

# Create 10 reusable profiles
profile_dir = "profiles"
if not os.path.exists(profile_dir):
    os.makedirs(profile_dir)
    for i in range(10):
        os.makedirs(os.path.join(profile_dir, f"profile_{i}"))

profile_index = 0

def visit_url(url):
    global profile_index
    chrome_options = Options()
    user_data_dir = os.path.join(profile_dir, f"profile_{profile_index}")
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    profile_index = (profile_index + 1) % 10
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=chrome_options,
    )
    driver.get(url)
    print(f"Visited {url}")
    driver.quit()

# Use ThreadPoolExecutor to visit URLs in parallel using submit
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(visit_url, url) for url in urls]
    concurrent.futures.wait(futures)
