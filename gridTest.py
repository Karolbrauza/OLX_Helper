import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

# List of URLs to visit
urls = [
    "https://www.olx.pl/d/mojolx/",
    "https://www.olx.pl/d/mojolx/",
    "https://www.olx.pl/d/mojolx/",
    "https://www.olx.pl/d/mojolx/",
    "https://www.olx.pl/d/mojolx/"
]

chrome_options = Options()

def visit_url(url):
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
