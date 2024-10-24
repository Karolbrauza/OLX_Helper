# OLXHelper

In need of additional function "Holiday" on polish marketplace olx.pl I created this helper where I would like add more missing functionalities. 

Functions list with short description:
- Holiday: go through all offers adding text to description eg. "I'm on holiday untill xx.xx.xxx", and increase price by specified value to handle extra costs of shipping during holiday or to aware customers of making orders if we i crease price for eg. 1000.

## New Feature: Parallel Processing

To improve the speed of processing multiple offers, the code now utilizes parallel processing using `concurrent.futures.ThreadPoolExecutor`. This allows multiple offers to be processed simultaneously, significantly reducing the overall processing time.

### How It Works

1. The `main.py` script now includes a `process_offer` function that encapsulates the logic for processing a single offer.
2. The `for` loop in `main.py` has been replaced with a `concurrent.futures.ThreadPoolExecutor` to handle multiple offers simultaneously.
3. The methods in `methods.py` that interact with web elements have been adapted to support parallel execution by adding necessary locks or synchronization mechanisms.
4. Each thread creates a new WebDriver instance to avoid conflicts and ensure thread safety.
5. The script uses a headless browser like `pyppeteer` or `Playwright` for better concurrency and parallel execution.

### Benefits

- **Speed**: Parallel processing allows multiple offers to be processed at the same time, reducing the total time required.
- **Efficiency**: By utilizing multiple threads, the script can handle a large number of offers more efficiently.
- **Thread Safety**: Creating a new WebDriver instance for each thread ensures that there are no conflicts between threads.
- **Better Concurrency**: Using a headless browser like `pyppeteer` or `Playwright` improves concurrency and parallel execution.

### Usage

To use the new parallel processing feature, simply run the `main.py` script as usual. The script will automatically handle the offers in parallel.

## Setting Up Selenium Grid for Parallel Execution

To set up Selenium Grid for parallel execution, follow these steps:

1. **Download and install Selenium Grid**: Download the Selenium Server jar file from the official Selenium website. You can find it here. Save the file to a directory on your machine.
2. **Start the Selenium Grid Hub**: Open a terminal or command prompt and navigate to the directory where you saved the Selenium Server jar file. Run the following command to start the Selenium Grid Hub:
    ```sh
    java -jar selenium-server-<version>.jar hub
    ```
    Replace `<version>` with the actual version number of the Selenium Server jar file you downloaded.
3. **Start Selenium Grid Nodes**: Open additional terminal or command prompt windows for each node you want to start. In each window, navigate to the directory where you saved the Selenium Server jar file and run the following command to start a node:
    ```sh
    java -jar selenium-server-<version>.jar node --hub http://localhost:4444/grid/register
    ```
    Replace `<version>` with the actual version number of the Selenium Server jar file you downloaded. The `--hub` parameter specifies the URL of the Selenium Grid Hub.
4. **Configure the WebDriver to use Selenium Grid**: In your `main.py` file, modify the WebDriver initialization to use the Selenium Grid Hub URL. Replace the existing WebDriver initialization code with the following:
    ```python
    from selenium import webdriver
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

    # Set the URL of the Selenium Grid Hub
    grid_url = "http://localhost:4444/wd/hub"

    # Set the desired capabilities for the browser
    capabilities = DesiredCapabilities.CHROME.copy()

    # Create a new instance of the WebDriver using the Selenium Grid Hub URL and desired capabilities
    driver = webdriver.Remote(command_executor=grid_url, desired_capabilities=capabilities)
    ```
5. **Run your script**: Execute your `main.py` script as usual. The WebDriver will now use the Selenium Grid Hub to distribute the tests across the available nodes, allowing for parallel execution.

By following these steps, you can set up Selenium Grid for parallel execution and improve the speed of processing multiple offers.
